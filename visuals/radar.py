import plotly.graph_objects as go


def portfolio_radar_chart(factor_scores: dict):
    """
    factor_scores: dict[str, float]
    values should be in range 0–100
    """

    categories = list(factor_scores.keys())
    values = list(factor_scores.values())

    # 闭合雷达图
    categories += [categories[0]]
    values += [values[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Portfolio Profile",
            line=dict(color="#4da3ff"),
            fillcolor="rgba(77,163,255,0.35)",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
            )
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        height=420,
    )

    return fig
