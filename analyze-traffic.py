import pyshark
import pandas as pd


pcap_file = 'traffic.pcapng'

def pcap_to_dataframe(pcap_file):  
    cap = pyshark.FileCapture(pcap_file, display_filter='websocket.opcode == 1')
    data = []
    
    for pkt in cap:
        try:
            data.append({
                'timestamp': pkt.sniff_time,
                'source_ip': pkt.ip.src,
                'destination_ip': pkt.ip.dst,
                'message': pkt.websocket.payload
            })
        except AttributeError:
            continue
    
    return pd.DataFrame(data)

df = pcap_to_dataframe('traffic.pcapng')  
df.to_csv('websocket_messages.csv', index=False)
print(df.head())