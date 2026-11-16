# Phase 2 learning notes — simple English

Read these with the actual code, results and checkpoints. Reading notes is preparation, not evidence of individual understanding. Prepared implementation and notes use substantial owner/AI assistance; retain the prototype and member integration history.

## The project story

Phase 1 asked whether engineered-history tree models beat simple forecasts. Phase 2 asks whether neural sequence learning works and whether connected sensors add value. We do not assume DL beats ML, nor that graph attention beats the no-neighbour control.

Example: your sensor currently reports 60 mph. Its own history looks normal, but a connected sensor is slowing. The hypothesis is that neighbour information may help anticipate future change. This is an illustrative scenario, not a measured event from our experiment.

## Inputs and answers

There are 207 sensors, each with a speed every five minutes. Twelve observed slots become one history. The first/last observation is 55 minutes apart. At origin 08:00, the history starts 07:05 and ends 08:00; outputs cover 08:05 through 09:00. Nothing after 08:00 is an input.

Each history position has normalized speed and a flag saying whether the original reading was missing. Five calendar inputs describe the forecast origin. A batch is [examples,12,207,2]; its answer tensor is [examples,12,207]. The next 12 speeds are regression targets, not classes.

We preserve the sensor order. Swapping columns while keeping a graph unchanged would attach one road's data to another road's neighbours, even if all array sizes still match.

## Missing readings and normalization

Zero/NaN means missing under the benchmark policy. Forward-fill inside each history; leading gaps use training sensor medians. Keep flags. Never fill missing future labels.

Normalization is (speed - training_mean) / training_std. The same global training statistics apply to validation, test and inference. We never fit them on future data. Convert predictions back to mph before reporting errors. A normalized speed of 0 is perfectly valid: it means the training mean, not a missing reading. That is why loss masking checks NaN labels, not normalized zeros.

The actual fitted mean is 58.5846 mph and standard deviation 12.8223 mph. For the previously studied 62.250-mph reading, the normalized input is approximately 0.286. These are training-fit statistics from the run manifest, not full-file fitting. The formal parameter counts are 3,912 for temporal GRU and 5,384 for graph GRU. Some retained attention-score parameters are inactive in self-only/uniform controls, so equal stored counts do not imply identical effective capacity.

## GRU: a small learned memory

A GRU reads the history in order and maintains a hidden state: a vector summarizing the past. Our vector has 32 numbers. These are learned representations, not 32 named traffic measurements.

We chose a compact GRU to give a clear temporal baseline with a small training budget. We did not train an LSTM or Transformer and cannot claim GRU is experimentally better than them. A small design makes the neighbour-access comparison easier to explain; it is not a proof of the best possible architecture.

- Update gate: controls how much previous state is retained versus replaced.
- Reset gate: controls how previous information enters the candidate state.
- Shared weights: every sensor uses the same learned sequence rules, while its different history produces a different hidden state.

The final hidden state and calendar features go to a linear output layer producing 12 corrections. We add these to the latest filled speed. Initially the correction layer is zero, so the initial forecast repeats that speed. This gives optimization a useful starting point, but it is not the optional ML-DL hybrid.

For a simple illustrative calculation, suppose the latest filled speed is 60 mph and the head learns corrections of -2 mph at 15 minutes and -5 mph at 60 minutes. The forecasts become 58 and 55 mph. These are teaching numbers, not measured forecasts. In code the addition happens in normalized units and is converted back to mph.

At initialization the output head is zero, so the first backward pass can update that head while gradients into earlier layers initially depend on its zero weights. As the head changes, gradients reach the GRU and graph layers. The tiny-fit diagnostic checks that the complete architecture can learn rather than merely produce arrays of the right size.

We predict all horizons directly. We do not feed the five-minute forecast back as if it were a measured reading to generate the next step.

## Graph attention: who can send information?

The supplied directed graph defines permitted connections. Our array is indexed [receiver,sender]. An entry allows the sender's learned history representation to enter the receiver's forecast. We transpose the supplied from-to adjacency to implement that convention. It is a coding convention, not proof that from/to has been independently labelled physical upstream/downstream.

GAT matches the project's graph-attention question and lets the model learn different weights among permitted neighbours. Equal-weight aggregation is a simpler alternative, so we actually test it rather than assuming learned weights help. We do not claim to have compared all graph-network families.

The layer projects each 32-number embedding, scores permitted sender/receiver pairs, applies softmax across senders and sums their vectors with those weights. Softmax weights are nonnegative and sum to 1 before dropout. Disallowed edges have weight 0. Self-loops let a sensor receive its own representation. Two attention heads make two learned aggregations, each 16 numbers; they are concatenated into 32 numbers.

We retain the local GRU embedding alongside the graph aggregate. The model can use its own history as well as the neighbour summary. Gaussian adjacency magnitudes select connectivity; they are not multiplied into or substituted for attention scores.

An attention picture describes model behaviour. It does not establish causal road influence or a measured congestion wave. This is original-style GAT, not a claim to implement a newer attention architecture or guarantee arbitrary dynamic neighbour rankings.

Illustrative attention example: if permitted sender embeddings are summarized as 10, 20 and 30 in one toy channel, weights .2, .3 and .5 give .2×10 + .3×20 + .5×30 = 23. Uniform weighting gives 20. The actual model aggregates learned vectors, not raw scalar speeds. During training, dropout can remove/rescale attention entries; the dropped row need not sum to one. At evaluation dropout is off and the pre-dropout softmax weights sum to one. These toy values are not evidence that learned attention beats uniform attention in our run.

## Training and tuning

Training learns weights by differentiating masked MAE. Backpropagation computes gradients. Adam updates weights. A learning rate controls update size. Weight decay discourages unnecessarily large weights; dropout randomly removes selected activations/attention entries during training. Evaluation turns dropout off.

Gradient clipping limits excessively large gradient norms. Early stopping retains the best tuning-validation checkpoint rather than blindly using the final epoch. We cap training at 50 epochs. Explicit dropout is necessary because an inter-layer dropout argument alone does nothing for a one-layer GRU.

The configuration declares two learning rates per architecture and fixed seeds. Model selection uses tuning validation only. Training optimizes all 12 horizons; selection summarizes 15/30/60 minutes. Therefore those two learning curves have different horizon aggregations and their height difference is not an exact generalization gap.

Training origins are strided by 2 to limit computation; all retained evaluation origins are used. Missing-only batches are skipped. We do not replace missing labels with zeros or score them as actual speeds.

Training-fit statistics end at the last training target. That timestamp equals the first tuning-validation origin; the first validation target is one step later. No validation target enters fitted statistics. Previously observed input history can cross a partition boundary.

Three-seed averages mean averages of three separately measured model scores, not an ensemble that averages their forecasts. The optional hybrid uses the predeclared seed 42 graph model, not whichever seed later scores best on test. Seed spread measures training randomness, not all uncertainty about future traffic.

An epoch means visiting the available strided training origins once, in a seeded shuffled order. Shuffling within the training partition is allowed; it does not move future validation/test samples into training. Each example already contains an ordered history. We do not carry a GRU hidden state from one shuffled example into the next: each window is encoded separately.

We save the checkpoint with the lowest headline tuning-validation MAE. Patience 7 means seven successive epochs without a new best score stop the fit; the 50-epoch cap can stop it earlier than that condition. The saved best epoch can differ from the last executed epoch. A seed fixes initialization and sample-order randomness, but does not promise identical numerical results on every device/library version.

## Ablations: test one explanation at a time

- Graph versus self-loops: retain the graph architecture but remove neighbour edges. This asks whether neighbour access helps.
- Learned versus uniform attention: allow the same neighbours but average them equally. This asks whether learned weighting helps beyond aggregation.
- Dropout versus no dropout: keep selected settings and remove dropout. This examines one regularizer. It is not proof that every regularization technique was useful.

The smaller temporal GRU is a useful architecture reference, but graph-versus-temporal alone mixes neighbour access with capacity changes. Self-only is the closer neighbour control. Some controls have one seed; do not describe them as robust multi-seed findings.

## How many models did we use?

There are six main comparison methods: four Phase 1 references/learned methods, temporal GRU and GRU+GAT. GAT is a component inside the graph forecasting model, not a separate forecast of its own. Self-only, uniform attention and no-dropout are controlled variants; the optional blend is a combination of two frozen forecasts.

For the neural study we evaluate 11 fits: three temporal seeds, three graph seeds, three self-only seeds, one uniform and one no-dropout. Learning-rate search adds two unselected candidates, giving 13 completed unique fits. Selected seed 42 candidates are reused, not trained and counted twice. Every neural fit shares weights across all 207 sensors; it is not 207 independently trained GRUs. This differs from Phase 1's per-sensor tree estimators.

## Optional hybrid

Mix XGBoost and graph predictions with one global weight. Select among 0,.25,.5,.75,1 on reserved validation, not test. Both endpoints are included. If an endpoint wins, blending has not shown benefit under this search. If an interior weight wins validation, still inspect its frozen test comparison; validation success does not guarantee test improvement.

This simple model combination is technically meaningful only if its rationale and measured behaviour are explained. It does not automatically earn additional marks.

## Evaluation

MAE: average error size in mph. RMSE: gives larger errors extra influence. MAPE: relative percentage error, unstable at low actual speeds. None is classification accuracy.

Report common valid targets, horizon curves, peak/off-peak, weekday/weekend and individual sensors. Check whether a small overall improvement hides worse peak behaviour or some sensors that regress. Retain negative values in signed improvement maps. Do not claim significance from millions of dependent overlapping forecasts; seed standard deviation is not a significance test.

The old test interval was inspected earlier. It remains exploratory even when the new tuning code is clean. A new untouched evaluation needs genuinely additional unexposed data; renaming the old interval cannot create it.

## LWR and the project title

Speed measures movement rate. Density measures vehicles per road length. Flow measures vehicles crossing per time. The relation q=rho*v links them under consistent definitions/units. Conservation says density changes when inflow and outflow differ.

LWR offers a macroscopic explanation of traffic waves, but METR-LA speed alone does not provide measured density/flow to calibrate the full model. We do not invent them. The forecasting component supplies no measured signal-control effects. A separate November16 synthetic CTM experiment now implements two rule-based signal agents; see PHASE2_CONTROL_NOTES.md. It is not calibrated LA traffic or GAT-driven control. Forecasting nodes are not control agents.

## Reproduction and responsibility

Use the runbook, actual configuration, tuning records and source/data/checkpoint hashes. A standalone forecast uses only the observed-history CSV and a fitted checkpoint; it does not need future labels. Reloaded checkpoints should reproduce predictions.

Each member should demonstrate their assigned module, identify one limitation and explain the end-to-end pipeline. Record actual review/implementation dates and assistance. Importing prepared files is not independent original authorship.

### Actual standalone forecast example

The selected graph seed 42 checkpoint (`tune_graph_0`, SHA-256 beginning `a 939480f`) was run with only the first 12 observed rows, ending March 1 2012 at 00:55. The last speeds for sensors 773869,767541,767542 were 62.250,67.750,66.875 mph. Its saved CSV gives:

| Target timestamp | Horizon | Sensor 773869 | Sensor 767541 | Sensor 767542 |
| --- | --- | --- | --- | --- |
| 2012-03-01 01:10 | 15min | 63.8972 | 65.7716 | 65.0641 |
| 2012-03-01 01:25 | 30min | 63.7686 | 65.5393 | 64.8767 |
| 2012-03-01 01:55 | 60min | 63.4805 | 65.3085 | 64.6830 |

These are actual forecasts in mph, not example targets. Future labels were unnecessary for this inference call. The dates lie inside the training interval, so this illustrates the input/output interface and is not independent generalization evidence. The full CSV has 207 sensor columns and 12 future rows; it stays local. The observed-history and window pipelines agree within float32-scale tolerance (maximum difference about 0.000011 mph); exact checkpoint reload is checked separately. See verification/phase2-20261112/observed_history_graph_check.json and the runbook for commands.

## Questions to practise

1. Why compare GRU with graph GRU, and why is a self-loop control necessary?
2. What does a hidden state mean? Why two attention heads?
3. Which direction does our message mask use?
4. Why are normalized zeros valid while raw zeros are treated as missing?
5. Which partition chooses learning rate, checkpoint and hybrid weight?
6. Why is the old test exploratory?
7. Can graph attention prove physical propagation or signal-control benefit?
8. What would you conclude if the graph, attention or hybrid fails to improve results?

Result-specific answers must come from the completed evidence, not predictions about which model should win.

## What our completed experiment actually found

At 60 minutes, mean MAE was 4.929 mph for temporal GRU, 4.881 for GRU+GAT and 4.931 for self-only. Neighbours reduced the graph model's error by about 0.050 mph versus its self-only control, approximately 1% of the self-only error. Three seeds showed a similar direction, but that is not a statistical significance test.

Our small neural models did **not** beat the strong tree methods. XGBoost's 60-minute MAE was 3.874 mph; Random Forest's was 3.896. Random Forest had the best main-model 60-minute RMSE, 7.255 mph, versus 9.619 for graph GRU. Say clearly that adding deep learning did not automatically produce the best forecasting system.

At seed 42, full graph MAE was 4.877, uniform neighbours 4.891 and no-dropout 4.847 mph. Learned attention slightly improved on equal weighting, but removing dropout improved this particular run. We cannot claim dropout helped every model or that a one-seed control proves a universally better setting.

The blend search selected XGBoost weight 1 and graph weight 0 on reserved validation. Therefore the selected forecast is pure XGBoost; blending did not demonstrate added value. We keep this unsuccessful hybrid result.

Metric trade-offs also matter. At 60 minutes, graph mean MAPE was 14.55%, versus 14.39% for persistence. Its lower MAE does not mean it improved every metric. For the seed 42 graph-versus-self comparison, 168 sensors improved and 39 worsened. Read the signed map rather than claiming every road benefited.

Possible limits include short history, compact shared architecture and bounded tuning. We did not run the experiments needed to identify which limit caused the gap to trees, so these are possible explanations rather than demonstrated causes. No negative neural forecasts occurred in this run; the unconstrained head still does not guarantee physical bounds on other inputs.

Use [measured tables](PHASE2_RESULTS.md), the final report and verification/phase2-20261112/all_metrics.csv as evidence. A defensible viva conclusion is: “Graph information gave a modest neural improvement under our fixed study, while the tree baselines remained stronger. We verified the comparison and reported both successes and failures.”


## Added LWR/control study — November16

Read [the simple control notes](PHASE2_CONTROL_NOTES.md) and [measured synthetic results](PHASE2_CONTROL_RESULTS.md). The updated sixth slide explains the eight-cell corridor and two local agents. The previous “no controller implemented” statement described the November13 forecasting-only study; it is superseded for this separate synthetic component. Neural scores remain unchanged.
