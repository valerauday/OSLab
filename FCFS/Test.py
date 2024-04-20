import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Define the FCFS algorithm logic
def fcfs_disk_scheduling(initial_head, request_sequence):
    total_seek_count = 0
    track_path = [(initial_head, 1)]

    current_head = initial_head
    for idx, track in enumerate(request_sequence):
        total_seek_count += abs(track - current_head)
        current_head = track
        track_path.append((track, idx + 2))

    return total_seek_count, track_path

# Create the Dash application
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FCFS Disk Scheduling Algorithm"),
    html.Div([
        html.Label("Initial Head Position:"),
        dcc.Input(id="initial-head", type="number", value=10),
    ]),
    html.Div([
        html.Label("Request Sequence (comma-separated):"),
        dcc.Input(id="request-sequence", type="text", placeholder="e.g., 14,28,33,23,17"),
    ]),
    html.Div(id='output-container'),
    dcc.Graph(id='track-path-graph')
])

# Callback to process input and generate output
@app.callback(
    [Output('output-container', 'children'),
     Output('track-path-graph', 'figure')],
    [Input('initial-head', 'value'),
     Input('request-sequence', 'value')]
)
def update_output(initial_head, request_sequence):
    if initial_head is None or request_sequence is None:
        return "", {}

    request_sequence = list(map(int, request_sequence.split(',')))

    total_seek_count, track_path = fcfs_disk_scheduling(initial_head, request_sequence)

    output_text = f"Total Seek Operations: {total_seek_count}"

    # Generate line graph showing the track path
    x = [point[0] for point in track_path]
    y = [point[1] for point in track_path]
    track_fig = go.Figure()
    track_fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Track Path'))
    track_fig.update_layout(title='Track Path', xaxis_title='Position', yaxis_title='Request Sequence',
                            xaxis=dict(tickvals=[initial_head] + request_sequence,
                                       ticktext=[f"Initial Head ({initial_head})"] + [str(track) for track in request_sequence]))
    
    return output_text, track_fig

if __name__ == '__main__':
    app.run_server(debug=True)
