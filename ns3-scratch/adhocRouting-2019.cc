/* 
 */

#include <fstream>
#include <vector>
#include <string>
#include <iostream>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/aodv-module.h"
#include "ns3/olsr-module.h"
#include "ns3/dsdv-module.h"
#include "ns3/dsr-module.h"
#include "ns3/applications-module.h"

#include "ns3/netanim-module.h"

using namespace ns3;
using namespace dsr;

NS_LOG_COMPONENT_DEFINE ("manet-routing-compare");

int
main (int argc, char *argv[])
{

  

  LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);

  //RngSeed=7497
  //RngRun=707

  int nSinks = 10; 	
  double txp = 7.5;	
  int protocol=1;//OLSR=1 AODV=2 DSR=3
  double interval=27.0010;
  double debit=0.5;
  int seed=1;
  int run=1;
  
  CommandLine cmd;

  cmd.AddValue ("protocol", "Routing protocol", protocol);
  cmd.AddValue ("debit", "Interval entre les paquets", debit);
  cmd.AddValue ("seed", "Rnd seed", seed);
  cmd.AddValue ("run", "Rnd run", run);

  cmd.Parse (argc, argv);

  ns3::RngSeedManager::SetSeed(seed);
  ns3::RngSeedManager::SetRun(run);

  interval=0.012/debit;

  printf("seed : %d", seed);

  Packet::EnablePrinting ();

  int nWifis = 20;     		//IFI: Nombre de noeuds

  double TotalTime = 100.0;	//IFI: Temps total des simulations
  std::string phyMode ("DsssRate11Mbps");
  std::string tr_name ("trace-ifi-ns3");
  double nodeSpeed = 0.1; //in m/s	//Vitesse maximum des noeuds du RWP 
  int nodePause = 0; //in s	//Pas de pause

  //Set Non-unicastMode rate to unicast mode
  Config::SetDefault ("ns3::WifiRemoteStationManager::NonUnicastMode",StringValue (phyMode));

  NodeContainer nodes;
  nodes.Create (nWifis);

  // setting up wifi phy and channel using helpers
  WifiHelper wifi;
  wifi.SetStandard (WIFI_PHY_STANDARD_80211b);

  YansWifiPhyHelper wifiPhy =  YansWifiPhyHelper::Default ();
  YansWifiChannelHelper wifiChannel;
  wifiChannel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel");
  wifiChannel.AddPropagationLoss ("ns3::FriisPropagationLossModel");
  wifiPhy.SetChannel (wifiChannel.Create ());

  // Add a non-QoS upper mac, and disable rate control
  //NqosWifiMacHelper wifiMac = NqosWifiMacHelper::Default ();
  WifiMacHelper wifiMac;

  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
                                "DataMode",StringValue (phyMode),
                                "ControlMode",StringValue (phyMode));

  wifiPhy.Set ("TxPowerStart",DoubleValue (txp));
  wifiPhy.Set ("TxPowerEnd", DoubleValue (txp));

  wifiMac.SetType ("ns3::AdhocWifiMac");
  NetDeviceContainer adhocDevices = wifi.Install (wifiPhy, wifiMac, nodes);

  MobilityHelper mobilityAdhoc;
  int64_t streamIndex = 0; // used to get consistent mobility across scenarios

  ObjectFactory pos;
  pos.SetTypeId ("ns3::RandomRectanglePositionAllocator");
  pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=300.0]"));
  pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=1500.0]"));

  Ptr<PositionAllocator> taPositionAlloc = pos.Create ()->GetObject<PositionAllocator> ();
  streamIndex += taPositionAlloc->AssignStreams (streamIndex);

  std::stringstream ssSpeed;
  ssSpeed << "ns3::UniformRandomVariable[Min=0.0|Max=" << nodeSpeed << "]";
  std::stringstream ssPause;
  ssPause << "ns3::ConstantRandomVariable[Constant=" << nodePause << "]";
  mobilityAdhoc.SetMobilityModel ("ns3::RandomWaypointMobilityModel",
                                  "Speed", StringValue (ssSpeed.str ()),
                                  "Pause", StringValue (ssPause.str ()),
                                  "PositionAllocator", PointerValue (taPositionAlloc));
  mobilityAdhoc.SetPositionAllocator (taPositionAlloc);
  mobilityAdhoc.Install (nodes);
  streamIndex += mobilityAdhoc.AssignStreams (nodes, streamIndex);

  AodvHelper aodv;
  OlsrHelper olsr;
  DsdvHelper dsdv;
  DsrHelper dsr;
  DsrMainHelper dsrMain;
  Ipv4ListRoutingHelper list;
  InternetStackHelper internet;

  switch (protocol)
    {
    case 1:
      list.Add (olsr, 100); //OLSR
      break;
    case 2:
      list.Add (aodv, 100); //AODV
      break;
    case 3:
      break;	//DSR
    default:
      NS_FATAL_ERROR ("No such protocol:" << protocol);
    }

  if (protocol < 3)
    {
      internet.SetRoutingHelper (list);
      internet.Install (nodes);
    }
  else if (protocol == 3)
    {
      internet.Install (nodes);
      dsrMain.Install (dsr, nodes);
    }

  NS_LOG_INFO ("assigning ip address");

  Ipv4AddressHelper addressAdhoc;
  addressAdhoc.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer adhocInterfaces;
  adhocInterfaces = addressAdhoc.Assign (adhocDevices);

  /* Setting applications */
  UdpEchoServerHelper echoServer (9);
  for (int i = 0; i <= nSinks - 1; i++)
    {
  	ApplicationContainer serverApps = echoServer.Install (nodes.Get (i));
  	serverApps.Start (Seconds (59.0));
  	serverApps.Stop (Seconds (91.0));

  	UdpEchoClientHelper echoClient (adhocInterfaces.GetAddress (i), 9);
  	echoClient.SetAttribute ("MaxPackets", UintegerValue (4000000000));
  	echoClient.SetAttribute ("Interval", TimeValue(Seconds(interval)));
  	echoClient.SetAttribute ("PacketSize", UintegerValue (1500));

  	ApplicationContainer clientApps = echoClient.Install (nodes.Get (i + 1));
  	clientApps.Start (Seconds (60.0));
  	clientApps.Stop (Seconds (90.0));
   }

  AsciiTraceHelper ascii;
  Ptr<OutputStreamWrapper> osw = ascii.CreateFileStream ( (tr_name + ".tr").c_str());
  wifiPhy.EnableAsciiAll (osw);

  NS_LOG_INFO ("Run Simulation.");


  AnimationInterface anim("anims/anim.xml");

  for (int i = 0; i <= 19; i++){
	anim.UpdateNodeSize (i, 17.0, 7.0);
  }

  

  Simulator::Stop (Seconds (TotalTime));
  Simulator::Run ();

  Simulator::Destroy ();
}

