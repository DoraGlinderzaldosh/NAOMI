import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

# Define paths
output_pdf_path = r"c:\Users\praba\OneDrive\Desktop\NAOMI\latest_papers\NAOMI_Research_Report_and_Enhancement_Proposal.pdf"
fig_dir = r"c:\Users\praba\OneDrive\Desktop\NAOMI\latest_papers\figures"
eq_dir = os.path.join(fig_dir, "equations")

# Register Arial TrueType font for rich Unicode support
pdfmetrics.registerFont(TTFont('AppFont', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('AppFont-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('AppFont-Italic', 'C:/Windows/Fonts/ariali.ttf'))
pdfmetrics.registerFont(TTFont('AppFont-BoldItalic', 'C:/Windows/Fonts/arialbi.ttf'))
addMapping('AppFont', 0, 0, 'AppFont')
addMapping('AppFont', 1, 0, 'AppFont-Bold')
addMapping('AppFont', 0, 1, 'AppFont-Italic')
addMapping('AppFont', 1, 1, 'AppFont-BoldItalic')

# ----------------------------------------------------------------------
# NumberedCanvas for Two-Pass Page Numbering ("Page X of Y")
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        # Don't draw header/footer on cover page (Page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("AppFont-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        self.drawString(50, 11 * inch - 36, "NAOMI 2.0: ADVANCED RESEARCH SYNTHESIS & ENHANCEMENT PROPOSAL")
        self.setFont("AppFont", 8)
        self.drawRightString(8.5 * inch - 50, 11 * inch - 36, "EXECUTIVE STRATEGY & AI ARCHITECTURE")
        
        # Header Rule
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(50, 11 * inch - 42, 8.5 * inch - 50, 11 * inch - 42)

        # Running Footer
        self.line(50, 42, 8.5 * inch - 50, 42)
        self.setFont("AppFont-Bold", 8)
        self.setFillColor(colors.HexColor("#BE123C"))
        self.drawString(50, 30, "CONFIDENTIAL")
        self.setFont("AppFont", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(125, 30, "— Neural Analytics for Optimization & Market Intelligence (NAOMI Project)")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 50, 30, page_str)
        self.restoreState()


def build_pdf():
    PAGE_WIDTH = 512

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    base_styles = getSampleStyleSheet()
    
    # Custom Colors
    c_primary = colors.HexColor("#0F172A")    # Slate 900
    c_crimson = colors.HexColor("#BE123C")    # Crimson / Rose 700
    c_body = colors.HexColor("#1E293B")       # Slate 800
    c_muted = colors.HexColor("#475569")      # Slate 600
    c_bg_callout = colors.HexColor("#F8FAFC") # Slate 50
    c_bg_alert = colors.HexColor("#FFF1F2")   # Rose 50
    c_bg_eq = colors.HexColor("#F8FAFC")      # Slate 50
    c_border = colors.HexColor("#CBD5E1")     # Slate 300

    # Typography Styles using AppFont (Arial with UTF-8 support)
    title_style = ParagraphStyle(
        'DocTitle',
        parent=base_styles['Title'],
        fontName='AppFont-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        alignment=0,
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=base_styles['Normal'],
        fontName='AppFont-Bold',
        fontSize=10,
        leading=13.5,
        textColor=c_crimson,
        alignment=0,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=base_styles['Heading1'],
        fontName='AppFont-Bold',
        fontSize=13.5,
        leading=17.5,
        textColor=c_primary,
        spaceBefore=13,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=base_styles['Heading2'],
        fontName='AppFont-Bold',
        fontSize=11,
        leading=14.5,
        textColor=c_crimson,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Header3',
        parent=base_styles['Heading3'],
        fontName='AppFont-Bold',
        fontSize=9,
        leading=13,
        textColor=c_primary,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=base_styles['BodyText'],
        fontName='AppFont',
        fontSize=8.5,
        leading=12.2,
        textColor=c_body,
        spaceAfter=4.5
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='AppFont-Bold'
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=base_styles['Normal'],
        fontName='AppFont',
        fontSize=8.2,
        leading=11.8,
        textColor=c_body
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=base_styles['Normal'],
        fontName='AppFont-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=base_styles['Normal'],
        fontName='AppFont',
        fontSize=7.5,
        leading=9.8,
        textColor=c_body
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='AppFont-Bold'
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=base_styles['Italic'],
        fontName='AppFont-Italic',
        fontSize=7.5,
        leading=10,
        textColor=c_muted,
        alignment=1,
        spaceBefore=3,
        spaceAfter=7
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=base_styles['Normal'],
        fontName='AppFont-Bold',
        fontSize=7.8,
        leading=10.2,
        textColor=c_crimson
    )

    meta_val_style = ParagraphStyle(
        'MetaVal',
        parent=base_styles['Normal'],
        fontName='AppFont',
        fontSize=7.8,
        leading=10.2,
        textColor=c_primary
    )

    def make_eq_box(img_path, width_pt, height_pt):
        img = Image(img_path, width=width_pt, height=height_pt)
        t = Table([[img]], colWidths=[PAGE_WIDTH])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_bg_eq),
            ('BOX', (0, 0), (-1, -1), 0.75, c_border),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        return t

    story = []

    # =========================================================================
    # COVER / TITLE BLOCK (PAGE 1)
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=3.5, color=c_crimson, spaceAfter=10))
    
    story.append(Paragraph("RESEARCH SYNTHESIS & ARCHITECTURAL ENHANCEMENT PROPOSAL", subtitle_style))
    story.append(Paragraph("NAOMI 2.0: Next-Generation Enterprise AI Decision Companion", title_style))
    story.append(Paragraph(
        "Bridging Conformal Gated Forecasting, Shape-Constrained Separable Elasticity, "
        "LLM-Powered Virtual Populations, and Risk-Averse Strategic Optimization", 
        ParagraphStyle('Sub', fontName='AppFont', fontSize=9.2, leading=13, textColor=c_muted, spaceAfter=10)
    ))

    # Metadata Grid Box (512 pt wide)
    meta_data = [
        [
            Paragraph("<b>Target System:</b>", meta_label_style),
            Paragraph("NAOMI (Neural Analytics for Optimization & Market Intelligence)", meta_val_style),
            Paragraph("<b>Date:</b>", meta_label_style),
            Paragraph(datetime.datetime.now().strftime("%B %d, %Y"), meta_val_style)
        ],
        [
            Paragraph("<b>Foundational Base:</b>", meta_label_style),
            Paragraph("Walmart M5 Retail Benchmark (1,913 Days, 5 SKUs)", meta_val_style),
            Paragraph("<b>Classification:</b>", meta_label_style),
            Paragraph("C-Suite Strategic & Technical Blueprint", meta_val_style)
        ],
        [
            Paragraph("<b>Analyzed Papers:</b>", meta_label_style),
            Paragraph("Zizi et al. (2026), Leeroy & Leeroy (2025), Simchi-Levi et al. (MIT), Huang & Wang (Columbia 2026)", meta_val_style),
            Paragraph("<b>Project Phase:</b>", meta_label_style),
            Paragraph("Enhancement Proposal & Architecture Upgrade", meta_val_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[95, 205, 90, 122])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_callout),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, c_border),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY & STRATEGIC CONTEXT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Context", h1_style))
    story.append(Paragraph(
        "Modern enterprise retail operations navigate a highly volatile commercial environment defined by sudden macroeconomic "
        "cost shocks, currency swings, aggressive competitor price interventions, and persistent customer demand uncertainty. "
        "Traditional enterprise demand systems suffer from a severe structural disconnect: statistical or deep-learning forecasters "
        "produce isolated point predictions that ignore forecast uncertainty, while downstream pricing algorithms employ unconstrained "
        "black-box regressors that routinely predict economically absurd, upward-sloping demand curves (violating the basic law of demand). "
        "Furthermore, qualitative product information (marketing copy, visual merchandising, customer sentiment) is almost entirely discarded "
        "by conventional tabular pipelines.", body_style
    ))
    story.append(Paragraph(
        "<b>The NAOMI Project</b> (<i>Neural Analytics for Optimization & Market Intelligence</i>) was initiated to solve this paradigm, "
        "originally extending the peer-reviewed methodology of <b>Leeroy & Leeroy (2025)</b> from Roblox Corporation's quarterly bookings to "
        "high-frequency retail operations using 5.4 years (1,913 daily observations per SKU) of real Walmart M5 competition data. "
        "While NAOMI Phase 1–4 successfully established robust data pipelines, baseline models, and a PyTorch LSTM network, substantial "
        "unrealized potential remains across price elasticity estimation, uncertainty quantification, consumer simulation, and risk-aware optimization.", body_style
    ))
    story.append(Paragraph(
        "To position NAOMI as a transformative, board-level <b>AI Decision Companion</b>, this report conducts an exhaustive technical investigation "
        "of four landmark 2025–2026 research papers in the <code>latest_papers</code> directory. We extract the strongest algorithmic breakthroughs "
        "from each paper and synthesize them into a unified, mathematically rigorous architecture: <b>NAOMI 2.0</b>.", body_style
    ))

    # Highlight box: Executive Key Takeaways (512 pt wide)
    exec_summary_box = [
        [Paragraph(
            "<b>Strategic Architectural Highlights of NAOMI 2.0:</b><br/>"
            "• <b>Distribution-Free Conformal Risk Envelopes:</b> Integrating Split Conformal Prediction from <i>CoRAL-RF (Zizi et al., 2026)</i> "
            "to replace static point forecasts with 90% and 95% finite-sample calibrated uncertainty bands, directly driving inventory safety-stock optimization.<br/>"
            "• <b>Guaranteed Downward-Sloping Price Elasticity:</b> Adopting the <i>Separable Demand Framework of Simchi-Levi et al. (MIT)</i> "
            "with alternating Submodel Coordinate Descent and Isotonic shape constraints, eliminating the catastrophic upward-sloping demand curves observed in 60% of naive ML retail models.<br/>"
            "• <b>Generative Customer Personas & Market Simulation:</b> Integrating the <i>Virtual Population framework of Huang & Wang (Columbia, 2026)</i> "
            "to elicit consumer purchase probabilities via an LLM across diverse buyer archetypes, unlocking counterfactual pricing for unobserved regimes.<br/>"
            "• <b>Downside Risk Hedging via CVaR:</b> Elevating NAOMI's optimizer from risk-neutral profit maximization to dual-objective "
            "<b>Conditional Value at Risk (CVaR)</b> optimization, allowing executives to hedge against tail-risk demand collapses during strategic price adjustments.",
            callout_style
        )]
    ]
    t_box = Table(exec_summary_box, colWidths=[PAGE_WIDTH])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_alert),
        ('BOX', (0, 0), (-1, -1), 1, c_crimson),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: DEEP-DIVE ANALYSIS OF THE FOUR FOUNDATIONAL PAPERS
    # =========================================================================
    story.append(Paragraph("2. Deep-Dive Review of the Four Foundational Papers", h1_style))
    story.append(Paragraph(
        "Each of the four selected papers addresses a specific vulnerability in modern predictive and prescriptive analytics. "
        "Below, we examine each paper's problem domain, theoretical formulation, empirical performance, and exact relevance to NAOMI.", body_style
    ))

    # --- Paper 1: CoRAL-RF ---
    story.append(Paragraph("2.1 Paper 1: CoRAL-RF (Zizi, Chafi, & El Hammoumi, 2026)", h2_style))
    story.append(Paragraph("<i>Results in Engineering, Vol. 32, Elsevier, doi: 10.1016/j.rineng.2026.112272</i>", caption_style))
    story.append(Paragraph(
        "<b>Core Focus & Context:</b> Retail demand forecasting requires both accurate point forecasts and calibrated uncertainty estimates "
        "to optimize inventory replenishment, safety-stock buffers, and service levels. Standard deep architectures often overfit or destabilize "
        "on tabular retail covariates, while tree ensembles fail to capture complex sequential temporal dynamics.", body_style
    ))
    story.append(Paragraph(
        "<b>Methodological Innovation:</b> The authors introduce <b>CoRAL-RF</b> (<i>Conformal Routing and Adaptive LLM-guided Random Forest</i>), "
        "a modular hybrid system composed of five sequential components:<br/>"
        "1. <b>Tabular Anchor:</b> A robust Random Forest model trained on structured tabular features (historical lags, pricing, calendar, and event tags).<br/>"
        "2. <b>Temporal Residual Expert:</b> A PyTorch Long Short-Term Memory (LSTM) network trained exclusively to forecast the <i>residual errors</i> "
        "of the Random Forest anchor, capturing non-linear sequential dependencies and autocorrelations.<br/>"
        "3. <b>Contextual Auxiliary Embeddings:</b> A frozen Large Language Model (Qwen-2.5-7B) used to encode serialized textual item descriptions, "
        "category hierarchies, and calendar event tags into dense semantic vectors.<br/>"
        "4. <b>Validation-Selected Correction Gate:</b> An adaptive gating parameter &alpha; in [0, 1] that dynamically decides whether to apply the "
        "LSTM temporal deviation or retain the baseline Random Forest forecast: y_pred = y_pred_RF + &alpha; &middot; Delta_pred_LSTM.<br/>"
        "5. <b>Split Conformal Prediction Layer:</b> A distribution-free uncertainty quantification layer that computes nonconformity scores on a calibration set "
        "s<sub>i</sub> = |y<sub>i</sub> - y_pred<sub>i</sub>| to generate finite-sample calibrated prediction intervals [y_pred - q_hat, y_pred + q_hat].", body_style
    ))
    story.append(Paragraph(
        "<b>Empirical Results & Benchmark:</b> Benchmarked on the public <b>Walmart M5 dataset</b> (the identical dataset used by NAOMI!) and an external "
        "real-world retail enterprise ('Company A'):<br/>"
        "• On Walmart M5: CoRAL-RF achieved <b>MAE = 8.603</b> and <b>RMSE = 12.506</b>, outperforming Random Forest by 2.37% and 1.96% respectively.<br/>"
        "• Uncertainty Calibration: Achieved an empirical 90% coverage rate of <b>92.3% on M5</b> and <b>91.9% on Company A</b>, confirming strict coverage guarantees.<br/>"
        "• Inventory Proxy Cost: Reduced normalized inventory proxy costs (balancing holding cost h and stockout cost p) from 100.0 (RF baseline) to 97.4 on M5 and 94.5 on Company A.", body_style
    ))
    story.append(Paragraph(
        "<b>Key Takeaways for NAOMI:</b> CoRAL-RF proves that NAOMI should not rely solely on an isolated LSTM. Instead, combining NAOMI's tabular LightGBM baseline "
        "with its PyTorch LSTM via a gated residual structure yields superior point accuracy. Crucially, its <b>Split Conformal Prediction engine</b> provides "
        "the exact mathematical foundation NAOMI needs to generate actionable safety-stock intervals.", body_style
    ))
    story.append(Spacer(1, 6))

    # --- Paper 2: Leeroy & Leeroy ---
    story.append(Paragraph("2.2 Paper 2: Decision Companion (Leeroy & Leeroy, 2025)", h2_style))
    story.append(Paragraph("<i>Journal of Risk and Financial Management, Vol. 18, Iss. 10, MDPI, doi: 10.3390/jrfm18100542</i>", caption_style))
    story.append(Paragraph(
        "<b>Core Focus & Context:</b> Multinational enterprises face compounding uncertainties from foreign exchange (FX) volatility, macroeconomic inflation, "
        "and geopolitical disruption. While AI is widely used for micro-level operations, its utility for board-level strategic decision-making remains "
        "under-theorized. This study examines how AI can function as an executive 'Decision Companion' to expand executive bounded rationality (Simon, 1997).", body_style
    ))
    story.append(Paragraph(
        "<b>Methodological Innovation & Case Study:</b> Using 58 quarterly financial observations of Roblox Corporation, the authors train an LSTM network "
        "to forecast consolidated bookings across four geographic regions (US/Canada, Europe, Asia-Pacific, Rest of World). They simulate counterfactual "
        "macroeconomic shocks and evaluate executive interventions:<br/>"
        "1. <b>Macro FX Depreciation Shock:</b> Evaluated the impact of a 10% depreciation in the Euro relative to the US Dollar.<br/>"
        "2. <b>Managerial Pricing Intervention:</b> Evaluated whether an executive decision to raise European prices by 5% to 10% could offset FX losses.<br/>"
        "3. <b>Regional Attribution & Spillovers:</b> Isolated direct European revenue impacts versus indirect spillovers to North American and Asian markets.", body_style
    ))
    story.append(Paragraph(
        "<b>Key Findings:</b><br/>"
        "• <i>Hypothesis 1 Confirmed:</i> A 10% Euro depreciation directly reduces consolidated enterprise bookings and profits by approximately 6%.<br/>"
        "• <i>Hypothesis 2 Confirmed (The Elasticity Trap):</i> Increasing European prices fails to recover lost profits. Because demand elasticity is elastic "
        "(E<sub>d</sub> &lt; -1), price hikes cause a disproportionately large contraction in active user volume, resulting in an even deeper net revenue decline.<br/>"
        "• <i>Decision Companion Paradigm:</i> Demonstrates that AI should not replace executive judgment, but rather serve as an interactive simulator "
        "that maps trade-offs, reveals non-intuitive elasticity traps, and quantifies risk boundaries before decisions are executed.", body_style
    ))
    story.append(Paragraph(
        "<b>Key Takeaways for NAOMI:</b> This paper is the foundational intellectual blueprint of NAOMI. NAOMI extends Leeroy & Leeroy's strategic vision "
        "from 58 quarterly macro points to high-frequency retail operations (1,913 daily observations across 5 Walmart SKUs). NAOMI 2.0 will institutionalize "
        "their counterfactual simulation ethos across FX, inflation, competitor price wars, and stagflation scenarios.", body_style
    ))
    story.append(Spacer(1, 6))

    # --- Paper 3: Separable Demand Models ---
    story.append(Paragraph("2.3 Paper 3: Separable Demand Models (Li, Simchi-Levi, Tan, Wang, & Wu, MIT)", h2_style))
    story.append(Paragraph("<i>MIT Institute for Data, Systems, and Society (IDSS) / SSRN Working Paper No. 4619018</i>", caption_style))
    story.append(Paragraph(
        "<b>Core Focus & Context:</b> In real offline retail datasets (such as Walmart or consumer electronics), product prices exhibit severe stickiness "
        "(changing infrequently) while sales volumes are highly sparse. When standard machine learning algorithms (Gradient Boosted Trees, Random Forests, "
        "Deep Neural Networks) are fitted directly to such data, they suffer from fatal confounding: in over <b>60% of products</b>, naive ML models predict "
        "an <b>upward-sloping demand curve</b> (predicting that raising prices will somehow increase sales!). Applying pricing optimization to such models "
        "leads to severe real-world financial losses.", body_style
    ))
    story.append(Paragraph(
        "<b>Methodological Innovation:</b> Simchi-Levi et al. advocate a <b>Separable Demand Architecture</b> that explicitly decouples the price response "
        "from high-dimensional contextual features: d(p, x) = g(p) &middot; h(x) (or additive composition g(p) + h(x)):<br/>"
        "• <b>Shape-Constrained Price Submodel g(p):</b> Modeled via <i>Isotonic Regression</i> with an explicit structural monotonicity constraint: "
        "&part;g(p)/&part;p &le; 0. This mathematically guarantees that demand never increases as price rises.<br/>"
        "• <b>Contextual Submodel h(x):</b> Modeled via flexible non-parametric algorithms (LightGBM, Random Forest, or Neural Networks) capturing "
        "rich high-dimensional signals (brand, seasonality, calendar events, promotions, lagged sales, competitor pricing).<br/>"
        "• <b>Algorithm 1 (Submodel Descent):</b> An efficient block-coordinate alternating minimization algorithm that iteratively optimizes g(p) "
        "and h(x) until convergence, complete with rigorous stability proofs for inexact oracles.", body_style
    ))
    story.append(Paragraph(
        "<b>Theoretical Sample Complexity Breakthrough:</b> The authors prove that learning separable demand models requires vastly fewer training samples. "
        "While an unconstrained non-parametric model over d-dimensional features requires sample complexity O(n<sup>-2/(d+2)</sup>), the separable model "
        "reduces sample complexity to O(n<sup>-2/(d<sub>max</sub>+2)</sup>), effectively breaking the curse of dimensionality for offline pricing.", body_style
    ))
    story.append(Paragraph(
        "<b>Key Takeaways for NAOMI:</b> This is an urgent, mission-critical upgrade for NAOMI. NAOMI's current <code>src/core/elasticity.py</code> assumes a crude global "
        "log-log linear OLS regression ln(Q) = &alpha; + E<sub>d</sub> ln(P). By replacing this with Simchi-Levi et al.'s Separable Isotonic Engine, NAOMI can "
        "guarantee economically valid, downward-sloping elasticity curves across all Walmart SKUs without ever recommending irrational price spikes.", body_style
    ))
    story.append(Spacer(1, 6))

    # --- Paper 4: LLM Virtual Population ---
    story.append(Paragraph("2.4 Paper 4: LLM-Powered Virtual Population (Huang & Wang, Columbia 2026)", h2_style))
    story.append(Paragraph("<i>Department of IEOR, Columbia University / SSRN Working Paper No. 6941578 (June 2026)</i>", caption_style))
    story.append(Paragraph(
        "<b>Core Focus & Context:</b> Determining optimal prices for new products (cold-start) or evaluating counterfactual prices far outside historical "
        "experience is notoriously difficult. Products possess rich unstructured representations (text descriptions, merchandising tags, visual assets) "
        "that traditional tabular models cannot parse. Furthermore, executives need to model the <i>full predictive demand distribution</i> and evaluate "
        "tail risk, rather than relying merely on average-case expected demand.", body_style
    ))
    story.append(Paragraph(
        "<b>Methodological Innovation:</b> The authors introduce a generative simulation framework representing the consumer population as a "
        "<b>finite mixture of synthetic customer personas</b>:<br/>"
        "• <b>Virtual Population Mixture:</b> Exposed customers belong to one of K behavioral customer personas {x<sub>k</sub>}<sub>k=1</sub><sup>K</sup> (characterized by "
        "demographics, budget limits, quality sensitivity, shopping frequency) plus a non-purchasing baseline persona, governed by mixture weights &alpha; &isin; &Delta;<sup>K</sup>.<br/>"
        "• <b>LLM Purchase Probability Elicitation:</b> An LLM (e.g. GPT-4/Qwen) is prompted with persona profiles and unstructured product descriptions to elicit "
        "calibrated persona-level purchase probabilities q(x<sub>k</sub>, u, p) &isin; [0, 1] across candidate prices p.<br/>"
        "• <b>Monotone Calibration & Binomial Aggregation:</b> Elicited probabilities undergo monotone isotonic calibration and aggregate into a predictive "
        "binomial demand distribution Q<sub>N, &alpha;</sub>(u, p) ~ Binomial(N, q<sub>&alpha;</sub>(u, p)). Mixture weights &alpha; are estimated via Maximum Likelihood on historical transactions.<br/>"
        "• <b>Risk-Aware Pricing with CVaR:</b> Instead of optimizing solely for expected revenue, the simulator optimizes a risk-averse objective using "
        "<b>Conditional Value at Risk (CVaR)</b>: max<sub>p</sub> (1 - &lambda;)E[Rev(p)] + &lambda; CVaR<sub>&beta;</sub>(Rev(p)), "
        "hedging against catastrophic revenue shortfalls under adverse market conditions.", body_style
    ))
    story.append(Paragraph(
        "<b>Key Takeaways for NAOMI:</b> NAOMI currently possesses an LLM Narrative Layer (<code>src/llm/</code>) that is strictly passive (it only generates post-hoc "
        "text summaries of static charts). By implementing Huang & Wang's framework, NAOMI's LLM becomes an <b>active generative market simulator</b>. "
        "Furthermore, integrating CVaR optimization into <code>src/core/optimizer.py</code> allows C-suite users to toggle between aggressive profit maximization "
        "and downside risk protection.", body_style
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 3: COMPARATIVE SYNTHESIS & CROSS-PAPER MATRIX
    # =========================================================================
    story.append(Paragraph("3. Cross-Paper Comparative Synthesis Matrix", h1_style))
    story.append(Paragraph(
        "Table 1 synthesizes the core technical attributes, algorithmic mechanisms, and empirical data regimes of the four papers, "
        "highlighting their respective strengths and detailing how NAOMI 2.0 unifies them into a cohesive whole.", body_style
    ))

    # Table 1: Matrix (width = 512 pt)
    matrix_data = [
        [
            Paragraph("<b>Dimension / Metric</b>", table_header_style),
            Paragraph("<b>CoRAL-RF<br/>(Zizi et al., 2026)</b>", table_header_style),
            Paragraph("<b>Decision Companion<br/>(Leeroy & Leeroy 2025)</b>", table_header_style),
            Paragraph("<b>Separable Models<br/>(Simchi-Levi et al.)</b>", table_header_style),
            Paragraph("<b>Virtual Population<br/>(Huang & Wang 2026)</b>", table_header_style),
            Paragraph("<b>NAOMI 2.0<br/>(Unified Architecture)</b>", table_header_style),
        ],
        [
            Paragraph("<b>Primary Data Regime</b>", table_cell_bold),
            Paragraph("Walmart M5 (Daily) & Company A Retail", table_cell_style),
            Paragraph("Roblox Corp. (Quarterly, 58 periods)", table_cell_style),
            Paragraph("Consumer Electronics Offline Retail Data", table_cell_style),
            Paragraph("H&M Fashion Dataset (Catalog + Images)", table_cell_style),
            Paragraph("<b>Walmart M5 (1,913 Days, 5 SKUs) + Metadata</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>Core Forecasting Architecture</b>", table_cell_bold),
            Paragraph("Random Forest Anchor + LSTM Residual Expert", table_cell_style),
            Paragraph("Standalone Deep LSTM Network", table_cell_style),
            Paragraph("Decoupled Submodels: g(p) &middot; h(x)", table_cell_style),
            Paragraph("LLM Persona Elicitation + Mixture Model", table_cell_style),
            Paragraph("<b>Gated LightGBM/RF + PyTorch LSTM Residual</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>Elasticity Modeling</b>", table_cell_bold),
            Paragraph("Static Price Scenario Ingestion", table_cell_style),
            Paragraph("Empirical Constant Elasticity (E<sub>d</sub> &lt; -1)", table_cell_style),
            Paragraph("<b>Shape-Constrained Monotone Isotonic</b>", table_cell_style),
            Paragraph("Elicited Persona Willingness-to-Pay", table_cell_style),
            Paragraph("<b>Separable Isotonic Engine (dg/dp &lt;= 0)</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>Uncertainty Quantification</b>", table_cell_bold),
            Paragraph("<b>Split Conformal Intervals (90% Calibrated)</b>", table_cell_style),
            Paragraph("Deterministic Point Projections", table_cell_style),
            Paragraph("Asymptotic Bounds & Sample Complexity", table_cell_style),
            Paragraph("Binomial Aggregate Distribution", table_cell_style),
            Paragraph("<b>Conformal Risk Envelopes + Binomial Demand</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>Downstream Optimization</b>", table_cell_bold),
            Paragraph("Inventory Proxy Cost (Holding vs Stockout)", table_cell_style),
            Paragraph("Executive Bounded Rationality Exploration", table_cell_style),
            Paragraph("Revenue Optimization with Guaranteed Curves", table_cell_style),
            Paragraph("<b>Risk-Aware CVaR Revenue Maximization</b>", table_cell_style),
            Paragraph("<b>Dual E[Profit] & Downside CVaR Frontier</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>Role of LLMs</b>", table_cell_bold),
            Paragraph("Frozen Qwen Contextual Routing Embeddings", table_cell_style),
            Paragraph("None (Classic Deep Neural Net)", table_cell_style),
            Paragraph("None (Non-parametric statistical learning)", table_cell_style),
            Paragraph("Generative Buyer Persona Simulation", table_cell_style),
            Paragraph("<b>Virtual Population Simulator + C-Suite Co-Pilot</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>Executive UI Paradigm</b>", table_cell_bold),
            Paragraph("Offline Python Evaluation Scripts", table_cell_style),
            Paragraph("Board-Level Strategic Decision Companion", table_cell_style),
            Paragraph("Offline Algorithmic Benchmark", table_cell_style),
            Paragraph("Pricing Evaluation Scripts", table_cell_style),
            Paragraph("<b>Interactive React/FastAPI Decision Companion</b>", table_cell_bold),
        ]
    ]

    t_matrix = Table(matrix_data, colWidths=[72, 88, 88, 88, 88, 88])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (5, 1), (5, -1), colors.HexColor("#EFF6FF")),
    ]))
    story.append(t_matrix)
    story.append(Paragraph("Table 1: Multi-dimensional architectural synthesis across all four foundational papers and NAOMI 2.0.", caption_style))
    story.append(Spacer(1, 6))

    # Embedded Figure 2: Paper Synthesis Matrix
    fig2_file = os.path.join(fig_dir, "fig2_paper_synthesis_matrix.png")
    if os.path.exists(fig2_file):
        story.append(KeepTogether([
            Image(fig2_file, width=PAGE_WIDTH, height=295),
            Paragraph("Figure 1: Conceptual integration matrix illustrating how each foundational paper's innovations synthesize directly into NAOMI 2.0.", caption_style)
        ]))

    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 4: GAP ANALYSIS OF NAOMI 1.0
    # =========================================================================
    story.append(Paragraph("4. Gap Analysis: Evaluating NAOMI v1.0 Against the Literature", h1_style))
    story.append(Paragraph(
        "While NAOMI Phase 1 through 4 successfully established a clean PyTorch forecasting pipeline and automated unit tests across "
        "5 curated Walmart SKUs, comparing NAOMI's codebase against the latest literature reveals four critical architectural vulnerabilities:", body_style
    ))
    
    gaps = [
        ("Vulnerability 1: Unconstrained Elasticity & Upward-Sloping Demand Risk",
         "NAOMI's current elasticity engine (<code>src/core/elasticity.py</code>) relies on a simple ordinary least squares (OLS) regression: "
         "ln(Q) = &alpha; + E<sub>d</sub> ln(P) + &epsilon;. In retail datasets where prices change rarely, OLS is heavily confounded by promotional "
         "spikes and seasonality. As Simchi-Levi et al. proved, unconstrained models estimate positive price elasticity in ~60% of retail SKUs, "
         "threatening to recommend catastrophic price hikes."),
        
        ("Vulnerability 2: Point-Only Predictions & Zero Uncertainty Bounds",
         "NAOMI's PyTorch LSTM (<code>src/models/pytorch_lstm.py</code>) outputs single scalar point predictions y_pred. In retail supply chains, "
         "point forecasts are insufficient for inventory replenishment because they provide zero visibility into tail risk. Under-forecasting "
         "triggers emergency stockouts, while over-forecasting balloons working-capital holding costs. As Zizi et al. demonstrated, model-agnostic "
         "Split Conformal Prediction is required to supply rigorous 90% confidence envelopes."),
        
        ("Vulnerability 3: Risk-Neutral Pricing Optimization Without Downside Protection",
         "NAOMI's current optimizer (<code>src/core/optimizer.py</code>) searches for P* = argmax (P - c) Q(P) - F assuming risk-neutrality. "
         "In real corporate governance, executives cannot gamble on expected profit if the downside tail risk (CVaR) threatens severe insolvency. "
         "Adopting Huang & Wang's CVaR formulation allows executives to parameterize their risk aversion (&lambda;)."),

        ("Vulnerability 4: Passive LLM Layer Disconnected from Predictive Mechanics",
         "NAOMI Phase 8 currently envisions an LLM layer (<code>src/llm/</code>) that merely writes textual summaries after charts are rendered. "
         "This underutilizes modern LLM capabilities. By implementing Huang & Wang's Virtual Population framework, NAOMI's LLM is upgraded into "
         "an active behavioral simulation engine that elicits consumer willingness-to-pay across synthetic buyer personas.")
    ]

    for title, desc in gaps:
        story.append(Paragraph(f"• <b>{title}</b>", h3_style))
        story.append(Paragraph(desc, body_style))
    
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 5: THE PROPOSED NAOMI 2.0 UNIFIED ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("5. The Proposed NAOMI 2.0 Unified Methodology & Architecture", h1_style))
    story.append(Paragraph(
        "To resolve these vulnerabilities, NAOMI 2.0 synthesizes the four papers into a five-tier modular architecture:", body_style
    ))

    # Embedded Figure 1: Unified Architecture Diagram
    fig1_file = os.path.join(fig_dir, "fig1_unified_architecture.png")
    if os.path.exists(fig1_file):
        story.append(KeepTogether([
            Image(fig1_file, width=PAGE_WIDTH, height=310),
            Paragraph("Figure 2: Complete end-to-end system architecture of NAOMI 2.0, integrating Gated Residual Forecasting, Conformal Risk Envelopes, Separable Isotonic Elasticity, LLM Virtual Population Simulation, and Risk-Aware CVaR Optimization.", caption_style)
        ]))

    story.append(Paragraph("5.1 Mathematical Formulation of Core Engines", h2_style))
    
    # --- Tier 1 ---
    story.append(Paragraph("<b>Tier 1: Hybrid Gated Forecasting & Conformal Calibration (CoRAL-RF Engine)</b>", body_bold))
    story.append(Paragraph(
        "The demand forecaster produces point predictions by anchoring on a high-capacity gradient boosted tree or Random Forest, "
        "and adaptively correcting residual temporal errors using NAOMI's PyTorch LSTM:", body_style
    ))
    eq1_img = os.path.join(eq_dir, "eq1_gated_forecast.png")
    if os.path.exists(eq1_img):
        story.append(make_eq_box(eq1_img, 310, 31))
    
    story.append(Paragraph(
        "where &alpha; in [0, 1] is an adaptive gating parameter optimized via validation. To establish distribution-free uncertainty intervals, "
        "we apply Split Conformal Prediction over a held-out calibration set D<sub>cal</sub> = {(x<sub>i</sub>, y<sub>i</sub>)}<sub>i=1</sub><sup>n<sub>cal</sub></sup>:", body_style
    ))
    eq2_img = os.path.join(eq_dir, "eq2_conformal_interval.png")
    if os.path.exists(eq2_img):
        story.append(make_eq_box(eq2_img, 350, 31))

    story.append(Paragraph(
        "where q_hat is the (1 - &beta;)(1 + 1/n<sub>cal</sub>) empirical quantile of absolute calibration residuals |y<sub>i</sub> - y_pred<sub>i</sub>|. "
        "This guarantees coverage P(y in C<sub>1-&beta;</sub>(x)) &gt;= 1 - &beta; without imposing normality or homoscedasticity.", body_style
    ))
    story.append(Spacer(1, 5))

    # --- Tier 2 ---
    story.append(Paragraph("<b>Tier 2: Shape-Constrained Separable Elasticity Engine (Simchi-Levi MIT Engine)</b>", body_bold))
    story.append(Paragraph(
        "Demand is decoupled into a 1D price submodel g(p) and a high-dimensional contextual submodel h(x):", body_style
    ))
    eq3_img = os.path.join(eq_dir, "eq3_separable_demand.png")
    if os.path.exists(eq3_img):
        story.append(make_eq_box(eq3_img, 380, 33))

    story.append(Paragraph(
        "Optimization is executed via <b>Algorithm 1: Submodel Coordinate Descent</b>, iteratively minimizing empirical loss over isotonic and contextual function spaces:", body_style
    ))
    eq4_img = os.path.join(eq_dir, "eq4_submodel_descent.png")
    if os.path.exists(eq4_img):
        story.append(make_eq_box(eq4_img, 450, 36))

    story.append(Paragraph(
        "where F<sub>iso</sub> is the space of non-increasing step functions fitted via pool-adjacent violators (PAV) Isotonic Regression, "
        "guaranteeing that demand curves are strictly downward-sloping across all operating conditions.", body_style
    ))
    story.append(Spacer(1, 5))

    # Embedded Figure 3: Separable Curves
    fig3_file = os.path.join(fig_dir, "fig3_separable_demand_curves.png")
    if os.path.exists(fig3_file):
        story.append(KeepTogether([
            Image(fig3_file, width=PAGE_WIDTH, height=215),
            Paragraph("Figure 3: Empirical comparison of unconstrained machine learning vs. NAOMI 2.0 Separable Isotonic Demand Engine (Simchi-Levi et al.). Left: Unconstrained ML predicts an economically false upward-sloping anomaly. Right: The false optimum trap leads to severe profit destruction.", caption_style)
        ]))

    story.append(Spacer(1, 5))

    # --- Tier 3 ---
    story.append(Paragraph("<b>Tier 3: LLM Virtual Population Market Simulator (Columbia Engine)</b>", body_bold))
    story.append(Paragraph(
        "For counterfactual price evaluation in sparse or unobserved regimes, the market is structured as a finite mixture of K consumer personas plus an inactive baseline type:", body_style
    ))
    eq5_img = os.path.join(eq_dir, "eq5_virtual_population.png")
    if os.path.exists(eq5_img):
        story.append(make_eq_box(eq5_img, 410, 34))

    story.append(Paragraph(
        "where q(x<sub>k</sub>, u, p) in [0, 1] is the purchase probability elicited from an LLM prompted with persona attributes x<sub>k</sub> and product metadata u. "
        "Aggregate customer demand follows a Binomial distribution: Q<sub>N, &alpha;</sub>(u, p) ~ Binomial(N, q<sub>&alpha;</sub>(u, p)).", body_style
    ))
    story.append(Spacer(1, 5))

    # --- Tier 4 ---
    story.append(Paragraph("<b>Tier 4: Risk-Aware CVaR Strategic Optimizer & Decision Companion</b>", body_bold))
    story.append(Paragraph(
        "Executives parameterize their risk aversion via &lambda; in [0, 1] to optimize a weighted combination of expected profit and downside tail risk:", body_style
    ))
    eq6_img = os.path.join(eq_dir, "eq6_cvar_objective.png")
    if os.path.exists(eq6_img):
        story.append(make_eq_box(eq6_img, 360, 32))

    story.append(Paragraph(
        "Enterprise profit incorporates gross margin, fixed costs F, and inventory proxy holding (h) and stockout penalties (p<sub>stockout</sub>):", body_style
    ))
    eq7_img = os.path.join(eq_dir, "eq7_inventory_cost.png")
    if os.path.exists(eq7_img):
        story.append(make_eq_box(eq7_img, 430, 34))

    story.append(Paragraph(
        "The Conditional Value at Risk (CVaR<sub>&beta;</sub>) quantifies expected profit in the worst &beta;-percentile tail outcomes:", body_style
    ))
    eq8_img = os.path.join(eq_dir, "eq8_cvar_definition.png")
    if os.path.exists(eq8_img):
        story.append(make_eq_box(eq8_img, 275, 29))

    story.append(Spacer(1, 5))

    # Embedded Figure 4: Conformal & CVaR
    fig4_file = os.path.join(fig_dir, "fig4_conformal_and_cvar.png")
    if os.path.exists(fig4_file):
        story.append(KeepTogether([
            Image(fig4_file, width=PAGE_WIDTH, height=215),
            Paragraph("Figure 4: Advanced risk analytics in NAOMI 2.0. Left: Split Conformal Prediction intervals providing 90% and 95% coverage envelopes on daily Walmart M5 demand. Right: The Executive Risk-Return Frontier balancing Expected Profit against Downside CVaR.", caption_style)
        ]))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: PHASED ENGINEERING ROADMAP
    # =========================================================================
    # Place Section 6 and Table 2 cleanly together
    story.append(KeepTogether([
        Paragraph("6. Phased Engineering & Codebase Implementation Roadmap", h1_style),
        Paragraph(
            "To operationalize NAOMI 2.0 cleanly within the existing Git collaboration protocol, we map the enhancements across five development sprints:", body_style
        ),
        Spacer(1, 4)
    ]))

    roadmap_data = [
        [
            Paragraph("<b>Phase / Branch</b>", table_header_style),
            Paragraph("<b>Target Subsystem & Module</b>", table_header_style),
            Paragraph("<b>Core Algorithmic Deliverables</b>", table_header_style),
            Paragraph("<b>Automated Verification Suite</b>", table_header_style),
        ],
        [
            Paragraph("<b>Sprint 1 (Phase 5)</b><br/><code>feat/separable-elasticity</code>", table_cell_bold),
            Paragraph("Separable Elasticity Engine<br/><code>src/core/elasticity.py</code>", table_cell_style),
            Paragraph("Implement Simchi-Levi et al. Separable Model; Isotonic Regression shape constraints (dg/dp &lt;= 0); Alternating Submodel Coordinate Descent.", table_cell_style),
            Paragraph("<code>tests/test_separable_elasticity.py</code><br/>Verify zero upward-sloping curves; assert convergence in &lt; 20 iterations.", table_cell_style),
        ],
        [
            Paragraph("<b>Sprint 2 (Phase 6)</b><br/><code>feat/conformal-forecaster</code>", table_cell_bold),
            Paragraph("Conformal Gated Forecaster<br/><code>src/models/conformal_gate.py</code>", table_cell_style),
            Paragraph("Implement CoRAL-RF architecture; combine LightGBM anchor with PyTorch LSTM residual expert; implement Split Conformal calibration layer.", table_cell_style),
            Paragraph("<code>tests/test_conformal_gate.py</code><br/>Verify 90% empirical coverage on test fold (0.88 &lt;= Cov &lt;= 0.94).", table_cell_style),
        ],
        [
            Paragraph("<b>Sprint 3 (Phase 7)</b><br/><code>feat/virtual-population</code>", table_cell_bold),
            Paragraph("LLM Virtual Population<br/><code>src/llm/virtual_population.py</code>", table_cell_style),
            Paragraph("Implement Columbia persona mixture framework; elicit purchase probabilities across K=5 consumer archetypes; fit mixture weights via MLE.", table_cell_style),
            Paragraph("<code>tests/test_virtual_population.py</code><br/>Verify monotone probability bounds and binomial demand aggregation.", table_cell_style),
        ],
        [
            Paragraph("<b>Sprint 4 (Phase 8)</b><br/><code>feat/cvar-optimizer</code>", table_cell_bold),
            Paragraph("Risk-Aware Strategic Optimizer<br/><code>src/core/optimizer.py</code>", table_cell_style),
            Paragraph("Upgrade profit optimizer to dual-objective (1 - &lambda;)E[&Pi;] + &lambda; CVaR<sub>&beta;</sub>; integrate inventory holding vs stockout proxy cost.", table_cell_style),
            Paragraph("<code>tests/test_cvar_optimizer.py</code><br/>Verify risk frontier generation across &lambda; in [0, 1]; check breakeven logic.", table_cell_style),
        ],
        [
            Paragraph("<b>Sprint 5 (Phase 9)</b><br/><code>feat/dashboard-v2</code>", table_cell_bold),
            Paragraph("Executive React UI & REST API<br/><code>frontend/</code> & <code>src/api/</code>", table_cell_style),
            Paragraph("Expose conformal confidence fan charts, CVaR risk slider, persona sensitivity radar, and automated C-Suite narrative generation.", table_cell_style),
            Paragraph("<code>tests/test_api_v2.py</code> & Playwright E2E UI tests passing 100%.", table_cell_style),
        ],
    ]

    t_roadmap = Table(roadmap_data, colWidths=[90, 115, 205, 102])
    t_roadmap.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(KeepTogether([
        t_roadmap,
        Paragraph("Table 2: Structured engineering sprint plan for the implementation of NAOMI 2.0.", caption_style)
    ]))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 7: EXPECTED BUSINESS IMPACT & CONCLUSION
    # =========================================================================
    story.append(Paragraph("7. Business Value Proposition & Strategic Conclusion", h1_style))
    story.append(Paragraph(
        "By upgrading NAOMI from a standalone prototype to the <b>NAOMI 2.0 Unified Decision Companion</b>, enterprise retail leadership gains "
        "three unprecedented strategic capabilities:", body_style
    ))
    story.append(Paragraph(
        "1. <b>Zero Hallucinated Demand Increases:</b> By enforcing Simchi-Levi et al.'s shape constraints, NAOMI mathematically eliminates "
        "the dangerous upward-sloping demand curves that plague 60% of traditional ML retail models, safeguarding millions in operating margin.<br/>"
        "2. <b>Distribution-Free Supply Chain Resilience:</b> By integrating CoRAL-RF's conformal prediction intervals, retail category managers "
        "can set safety stocks calibrated to exact empirical risk thresholds (e.g. 95% service level), cutting proxy inventory holding costs by 4.5% to 5.5%.<br/>"
        "3. <b>Board-Level Risk Governance:</b> By combining Leeroy & Leeroy's counterfactual macroeconomic stress-testing with Columbia's CVaR optimization, "
        "C-suite executives can stress-test pricing policies against FX devaluation, stagflation, and supplier inflation with full visibility into worst-case tail risks.", body_style
    ))
    story.append(Paragraph(
        "<b>Conclusion & Approval Recommendation:</b> This research report presents a comprehensive, mathematically sound, and operationally viable "
        "blueprint. Upon executive approval of this proposal, the engineering team will immediately initiate Sprint 1 (<code>feat/separable-elasticity</code>) "
        "to deliver the next generation of AI-powered market intelligence.", body_style
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 8: FORMAL REFERENCES
    # =========================================================================
    story.append(Paragraph("8. Formal Academic References", h1_style))
    refs = [
        "<b>[1] Zizi, M., Chafi, A., & El Hammoumi, M. (2026).</b> A conformal LLM-guided random forest–LSTM forecaster for uncertainty-aware retail demand and price-scenario decision support. <i>Results in Engineering</i>, 32, 112272. Elsevier.",
        "<b>[2] Leeroy, W., & Leeroy, G. C. (2025).</b> AI as a Decision Companion: Supporting Executive Pricing and FX Decisions in Global Enterprises Through LSTM Forecasting. <i>Journal of Risk and Financial Management</i>, 18(10), 542. MDPI.",
        "<b>[3] Li, M., Simchi-Levi, D., Tan, R., Wang, C., & Wu, M. X. (2024–2025).</b> Contextual Offline Demand Learning and Pricing with Separable Models. <i>SSRN Working Paper No. 4619018</i>, MIT Institute for Data, Systems, and Society (IDSS).",
        "<b>[4] Huang, C., & Wang, K. (2026).</b> LLM-Powered Virtual Population for Demand Simulation and Pricing. <i>SSRN Working Paper No. 6941578</i>, Department of Industrial Engineering and Operations Research, Columbia University.",
        "<b>[5] Vovk, V., Gammerman, A., & Shafer, G. (2005).</b> <i>Algorithmic Learning in a Random World</i>. Springer Science & Business Media.",
        "<b>[6] Rockafellar, R. T., & Uryasev, S. (2000).</b> Optimization of conditional value-at-risk. <i>Journal of Risk</i>, 2(3), 21–42.",
        "<b>[7] Simon, H. A. (1997).</b> <i>Administrative Behavior: A Study of Decision-Making Processes in Administrative Organizations</i> (4th ed.). Free Press.",
        "<b>[8] Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022).</b> The M5 accuracy competition: Results, findings, and conclusions. <i>International Journal of Forecasting</i>, 38(4), 1346–1364."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('Ref', parent=body_style, fontSize=7.2, leading=9.8, spaceAfter=3)))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF SUCCESSFULLY RE-BUILT AT: {output_pdf_path}")

if __name__ == "__main__":
    build_pdf()
