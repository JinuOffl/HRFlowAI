import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def analyze_and_visualize(data: list):
    df = pd.DataFrame(data)
    
    charts = []
    
    if 'check_in_time' in df.columns and 'check_out_time' in df.columns:
        # Convert to datetime
        df['check_in'] = pd.to_datetime(df['check_in_time'])
        df['check_out'] = pd.to_datetime(df['check_out_time'])
        df['hours'] = (df['check_out'] - df['check_in']).dt.total_seconds() / 3600
        
        # Plot Work Hours
        plt.figure(figsize=(10, 5))
        if 'date' in df.columns:
            plt.plot(df['date'], df['hours'], marker='o')
            plt.title('Daily Work Hours')
            plt.xlabel('Date')
            plt.ylabel('Hours')
            
            # Save to Base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            charts.append(img_str)
            plt.close()
            
    return df, charts