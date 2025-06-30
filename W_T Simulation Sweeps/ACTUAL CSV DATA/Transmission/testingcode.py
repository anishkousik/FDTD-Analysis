import pandas as pd
import altair as alt
import os

# List of CSV file names
file_names = [
    '/Users/anishkousik/Desktop/FDTD Analysis/ACTUAL CSV DATA/Transmission/Transmission_data_sweep_6.csv',
]

for file in file_names:
    df = pd.read_csv(file)
    df.columns = ['width', 'thickness', 'value']
    df['thickness'] = pd.to_numeric(df['thickness'], errors='coerce')
    df['width'] = pd.to_numeric(df['width'], errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(subset=['thickness', 'width', 'value'], inplace=True)

    df['thickness_um'] = (df['thickness'] * 1e6).round(3).astype(str) + ' µm'
    df['width_um'] = (df['width'] * 1e6).round(3).astype(str) + ' µm'

    chart_width = 800 if "sweep_1" in file else 600
    chart_height = 800 if "sweep_1" in file else 600

    base = alt.Chart(df).encode(
        x=alt.X('thickness_um:O',
                axis=alt.Axis(title='Thickness (µm)', labelAngle=0),
                scale=alt.Scale(paddingInner=0)),
        y=alt.Y('width_um:O',
                axis=alt.Axis(title='Width (µm)'),
                scale=alt.Scale(paddingInner=0))
    ).properties(
        title=f'Transmission Heatmap for {os.path.basename(file)}',
        width=chart_width,
        height=chart_height
    )

    if "sweep_3" in file:
        # Shade anomalous data black, color others with spectral scale
        heatmap_layer = base.mark_rect().encode(
            color=alt.condition(
                'datum.value < 0.8',
                alt.value('black'),
                alt.Color('value:Q', title='Transmission',
                          scale=alt.Scale(scheme='spectral', reverse=True))
            )
        )
        text_layer = base.mark_text(
            font='Courier New',
            fontSize=11,
            align='center',
            baseline='middle'
        ).encode(
            text=alt.Text('value:Q', format='.6f'),
            color=alt.condition('datum.value < 0.8', alt.value('white'), alt.value('black'))
        )
    else:
        heatmap_layer = base.mark_rect().encode(
            color=alt.Color('value:Q', title='Transmission',
                            scale=alt.Scale(scheme='spectral', reverse=True))
        )
        text_layer = base.mark_text(
            font='Courier New',
            fontSize=11,
            align='center',
            baseline='middle',
            color='black'
        ).encode(
            text=alt.Text('value:Q', format='.6f')
        )

    final_chart = (heatmap_layer + text_layer).interactive()

    output_filename = f"heatmap_detailed_{os.path.splitext(os.path.basename(file))[0]}.json"
    final_chart.save(output_filename)
    print(f"✅ Heatmap for {file} saved as '{output_filename}'")
