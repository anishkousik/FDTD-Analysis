import pandas as pd
import altair as alt
import os

# File paths (adjust as needed)
file_names = [
    '/Users/anishkousik/Desktop/FDTD Analysis/W_T Simulation Sweeps/Sweep_1_New Monitor/2D_mode_confinement_sweep_6.csv',
]

for file in file_names:
    df = pd.read_csv(file)

    # Ensure correct column names
    df = df.rename(columns={
        df.columns[0]: 'file_id',
        df.columns[1]: 'width',
        df.columns[2]: 'thickness',
        df.columns[3]: 'value'  # 'Confinement Factor (2D)' becomes 'value' for plotting
    })

    # Clean and convert
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
        title=f'Mode Confinement Heatmap for {os.path.basename(file)}',
        width=chart_width,
        height=chart_height
    )

    if "sweep_3" in file:
        # Black out anomalous data
        heatmap_layer = base.mark_rect().encode(
            color=alt.condition(
                'datum.value < 0.05',
                alt.value('black'),
                alt.Color('value:Q', title='Mode Confinement',
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
            color=alt.condition('datum.value < 0.05', alt.value('white'), alt.value('black'))
        )
    else:
        heatmap_layer = base.mark_rect().encode(
            color=alt.Color('value:Q', title='Mode Confinement',
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

    output_filename = f"mode_confinement_heatmap_{os.path.splitext(os.path.basename(file))[0]}.json"
    final_chart.save(output_filename)
    print(f"✅ Heatmap for {file} saved as '{output_filename}'")




