# Phase 2 viva guide for Team T072

This guide goes with the final Phase 2 report (`report/phase2/T072_Phase2_Report.pdf`) and the 13-slide deck (`slides/phase2/T072_Phase2.pptx`). It explains the whole project, each member's module, the results, and every reference, in plain language.

Read sections 1 to 4 and 8 to 10 whatever your module is. The viva is individual, and anyone can be asked about any part.

One rule before anything else: **only say what you can explain.** The code and experiments were prepared under Kavya's coordination with substantial AI assistance, and each of us integrated and reviewed one module. If asked who wrote something, say that. Do not claim you wrote a module alone. Reading this guide is not a substitute for opening the files of your module and running the checks yourself.

## 1. The project in one minute

Phase 1 predicted traffic speed with machine-learning models (Random Forest and XGBoost) that looked at one sensor at a time.

Phase 2 asks one deep-learning question: **does a neural network forecast better if it can also look at neighbouring sensors on the road network?**

- We trained two small networks on the METR-LA dataset. The **GRU** reads one sensor's last hour. **GRU + GAT** is the same network plus a graph-attention layer that lets each sensor use its neighbours.
- Neighbours help, but only a little: the 60-minute error drops from 4.931 to 4.881 mph (about 1%).
- Both networks are still worse than the Phase 1 XGBoost model (3.874 mph).
- We tested a hybrid (a blend of XGBoost and GRU + GAT). The best blend was XGBoost alone, so there is no hybrid gain.
- Separately, we built a small **LWR traffic simulation** with two signal agents, because the project title mentions LWR models and multi-agent control. It uses made-up traffic and is not connected to the forecasts.

## 2. Who presents what

| Slide | Topic | Presenter |
| --- | --- | --- |
| 1 | Title and the question | anyone (suggest Kavya) |
| 2 | What Phase 2 is about: Part A forecasting, Part B simulation | anyone |
| 3 | The whole project in one picture | anyone |
| 4 | The model in one picture | Bineet or Vridhi |
| 5 | Preparing the data | Vridhi |
| 6 | Building and training the two networks | Bineet |
| 7 | Evaluating fairly and testing the hybrid | Kavya |
| 8 | Literature review and reading the results | Anshuman |
| 9 | LWR simulation with two signal agents | Rudraksh |
| 10 | Result 1: networks against the Phase 1 models | Anshuman |
| 11 | Result 2: ablations and hybrid | Bineet and Kavya |
| 12 | Result 3: simulation | Rudraksh |
| 13 | What we learned and what we do not claim | anyone |

Every slide has speaker notes in simple English. Open the deck in PowerPoint and read the notes under each slide.

## 3. Words everyone must be able to explain

| Word | Meaning |
| --- | --- |
| Forecast horizon | How far ahead we predict. We report 15, 30 and 60 minutes. |
| MAE | Mean absolute error: the average size of the error, in mph. Lower is better. |
| RMSE | Root mean squared error: like MAE but large errors count more. |
| Persistence | The simplest forecast: "the speed stays as it is now". |
| Historical average | The usual speed for that sensor at that time of the week, from training data. |
| Training / tuning / test data | Training data teach the model. Tuning (validation) data are used to choose settings. Test data are used once at the end to report scores. |
| Leakage | Information from the future or from the test data slipping into training. It makes results look better than they are. |
| Epoch | One pass over the training data. |
| Seed | The starting number for the random generator. Different seeds give slightly different trained models. We used 42, 43 and 44. |
| Over-fitting | The model memorises the training data and does worse on new data. |
| Regularisation | Methods that reduce over-fitting: dropout, weight decay, early stopping. |
| Ablation | Remove one part of the model, train again, and see how much the error changes. |
| Hybrid | A combination of an ML model and a DL model. Ours is a weighted average of XGBoost and GRU + GAT. |
| Exploratory | Our word for the test scores, because the test period was already looked at in Phase 1. They are not a clean final estimate. |

## 4. The model, step by step

1. **Input.** For every sensor: the last 12 readings (55 minutes). Each reading is two numbers: the scaled speed, and a flag that says whether the reading was missing.
2. **GRU.** A recurrent network reads the 12 readings in order and keeps a memory of 32 numbers. It has two gates. The *reset gate* decides how much old memory is used to form a new proposal. The *update gate* decides how much old memory is kept and how much is replaced. After 12 steps the memory is a summary of that sensor. One GRU, with one set of weights, is used for all 207 sensors.
3. **Graph attention (only in GRU + GAT).** Each sensor looks at the summaries of its neighbours on the road graph. It gives each neighbour a score, turns the scores into weights that add up to one (softmax), and takes the weighted average. The weights are learned. The road graph only decides who is a neighbour. We use two attention heads of 16 numbers each.
4. **Output layer.** Takes the sensor's own summary, the neighbour summary (graph model only) and five calendar values. It outputs 12 numbers: a correction for each of the next 12 steps.
5. **Add the last speed.** The corrections are added to the last observed speed. The output weights start at zero, so before training the model says "no change", which is the persistence forecast.

Sizes: 3,912 parameters for the GRU, 5,384 for GRU + GAT. Small on purpose, so that training takes 15 to 25 minutes on a laptop and we could afford three seeds and several ablations.

The two attention heads are **not** the two signal agents of the simulation. Heads are part of a forecasting network. Agents are separate objects that choose a signal phase.

## 5. Each member's module

### 5.1 Vridhi Chaudhary: preparing the data

**Files:** `src/trafficml/data/neural.py`, `tests/test_neural.py`, `requirements-phase2.txt`.

**What it does.** Turns the raw speed table into inputs for the networks without leakage.

**How it works.**

1. Cut the data into windows: 12 readings in, the next 12 as answers.
2. Fill a missing input from an earlier reading in the same window. If there is none, use the sensor's median speed from the training period. Never fill from a later reading.
3. Scale speeds with the mean and standard deviation of the training period only.
4. Add a missing flag for every reading and five calendar values (time of day and day of week as sine and cosine, and a weekend flag).
5. Leave missing answers empty. They are skipped in the loss and in every score.

**Numbers.** 207 sensors, 34,272 five-minute time steps (1 March to 27 June 2012), 8.11% of readings missing. Split by time into 23,963 training, 1,701 tuning, 1,702 blend-selection and 6,850 test points. Eleven points are dropped before each boundary.

**Likely questions.**

- *Why split by time and not randomly?* Readings five minutes apart are almost the same. A random split would put near-copies of test readings into training.
- *Why drop 11 points at each boundary?* A forecast made just before a boundary has answers that fall inside the next part. Dropping those points keeps the parts separate.
- *Why not fill missing answers?* A filled answer is invented data. Scoring the model against invented answers would be meaningless.
- *Why use sine and cosine for time of day?* So that 23:55 and 00:00 are close together, as they are on a clock.
- *Why a missing flag?* So the network can tell a real reading from a filled one.
- *What do the tests check?* That scaling uses training data only, that filling never uses the future, that changing a future reading does not change a current input, and that missing answers are ignored.

### 5.2 Bineet Keshari: building and training the networks

**Files:** `src/trafficml/models/neural.py`, `scripts/run_phase2.py`, `configs/phase2.yaml`, `docs/PHASE2_PROTOCOL.md`.

**What it does.** Defines the GRU and the GRU + GAT model, and trains both in the same way so that the comparison is fair.

**How it works.**

1. The model is the one in section 4.
2. Loss: mean absolute error over the answers that are not missing.
3. Optimiser: Adam, learning rate 0.001, weight decay 0.0001, batch of 32 forecast points.
4. Regularisation: dropout 0.1, weight decay, gradient clipping at norm 5, early stopping after 7 epochs without improvement (at most 50 epochs). The best version on the tuning data is kept.
5. Two learning rates were tried (0.001 and 0.0003). The one with the lower tuning error was kept: 0.001 for both models.
6. Each main model is trained three times with seeds 42, 43 and 44.
7. Three ablations: self-loop only (no neighbours), uniform neighbours (no learned weights), no dropout.

**Numbers.** 3,912 and 5,384 parameters. Tuning error 3.335 mph (GRU) and 3.306 mph (GRU + GAT). All settings were written into the configuration file before training on real data.

**Likely questions.**

- *What do the GRU gates do?* The reset gate controls how much old memory enters the new proposal. The update gate controls how much old memory is kept.
- *Why a GRU and not an LSTM?* A GRU has fewer parameters and is simpler. We did not compare the two, so we do not claim it is better.
- *What is attention here?* A learned weighted average of the neighbours' summaries. The weights come from a small scoring function followed by softmax.
- *What does softmax do?* It turns a list of scores into positive weights that add up to one.
- *Why predict a correction and not the speed itself?* "No change" is already a reasonable forecast. The network only has to learn the improvement.
- *What is dropout?* During training, a random 10% of values are set to zero so the network cannot rely on any single value.
- *What is gradient clipping?* If an update step is too large, it is scaled down. This keeps recurrent networks from becoming unstable.
- *Why is the self-loop model the fair comparison?* It has exactly the same layers and number of parameters as GRU + GAT. Only the neighbours are removed. The plain GRU is smaller, so comparing with it mixes two changes.
- *Why did removing dropout help?* The model is very small and does not over-fit, so dropout only removed useful information. We kept our planned setting anyway, because changing it after seeing a test score would be tuning on the test data.

### 5.3 Kavya Katal: evaluating fairly, hybrid, checks and coordination

**Files:** `scripts/evaluate_phase2.py`, `scripts/predict_phase2.py`, `.github/workflows/tests.yml`, `verification/`.

**What it does.** Scores every method on the same answers, tests the hybrid, lets a saved model make a forecast, and keeps the results repeatable. Kavya also coordinated the project and combined all five modules.

**How it works.**

1. All six methods (four from Phase 1, two networks) are scored on identical test answers with MAE and RMSE.
2. Hybrid: `blend = w x XGBoost + (1 - w) x GRU+GAT`, with `w` from 0, 0.25, 0.5, 0.75, 1. The weight is chosen on data kept aside for this, then frozen before the test data are scored.
3. `predict_phase2.py` loads a trained network and forecasts the next 12 steps from a history file of 12 rows.
4. 76 automated tests run on GitHub for every pull request.

**Numbers.** About 1.25 million scored answers at each horizon. Blend error on the kept-aside data: 3.779 (pure GRU + GAT), 3.585, 3.438, 3.336, 3.288 (pure XGBoost). Chosen weight: 1.00. All 76 tests pass with the dataset present. On GitHub, 65 pass and 11 are skipped because the dataset is not uploaded there.

**Likely questions.**

- *Why did the hybrid fail?* A blend helps when both models are about equally good and make different mistakes. Here GRU + GAT is about 1 mph worse, so adding it only pulls XGBoost down.
- *Then why report it?* Phase 2 asks for a hybrid to be tested. We tested it properly and report the true outcome.
- *Why choose the blend weight on separate data?* If we chose it on the test data, the test score would be biased in our favour.
- *MAE or RMSE, which matters more?* They answer different questions. XGBoost has the lowest MAE. Random Forest has the lowest RMSE, so it makes fewer very large errors.
- *Is this accuracy?* No. This is regression. We report errors in mph, not classification accuracy.
- *Why are the scores called exploratory?* The test period was already examined in Phase 1, so it is no longer an untouched test.

### 5.4 Anshuman Mehta: literature review and reading the results

**Files:** `docs/PHASE2_LITERATURE.md`, `scripts/build_phase2_report.py`, `scripts/build_control_report.py`, report and learning notes.

**What it does.** Links each part of the design to published work, and turns the tables of numbers into findings.

**The findings to be able to state.**

1. Both networks beat persistence at every horizon (GRU + GAT: 11.0% less error at 15 minutes, 8.3% less at 60).
2. The Phase 1 tree models are better at every headline horizon. At 60 minutes GRU + GAT is 1.01 mph behind XGBoost.
3. From 45 minutes on, even the historical average (4.187 mph) beats the networks.
4. The gain from neighbours grows with the horizon: 0.011 mph at 5 minutes, 0.050 mph at 60.
5. Looking at sensors one by one, 168 of 207 do better when neighbours are available.
6. Every method is much worse in rush hours. GRU + GAT: 7.691 mph in peak periods, 4.174 mph outside them (60 minutes ahead).

**Likely questions.**

- *Why did deep learning lose to trees?* Our likely explanation, which we did not test: Phase 1 trains a separate model for every sensor, so each learns its own road's daily pattern. Our network shares one small set of weights across 207 sensors and is not told which sensor it is looking at. It is also very small and was tuned only lightly.
- *Why does the gain from neighbours grow with horizon?* A neighbour may show traffic that has not reached the sensor yet. That matters more the further ahead you predict. This is a reasonable reading, not something we proved.
- *Why not compare with the scores in the DCRNN paper?* They use different data splits, missing-data rules and training. The numbers are not comparable.
- *Does attention show how congestion spreads?* No. The weights describe what the trained model does. They are not proof of cause and effect on the road.

Section 7 below explains every reference.

### 5.5 Rudraksh Sharma: LWR simulation and two signal agents

**Files:** `src/trafficml/simulation/lwr.py`, `agents.py`, `experiment.py`, `scripts/run_control.py`, `configs/control.yaml`, `tests/test_control.py`.

**What it does.** Simulates a small road to show traffic-flow physics and two signals working on the same road. It is separate from the forecasting, because METR-LA has only speed and no vehicle counts or signal data.

**How it works.**

1. **Road.** Eight cells of 250 m. Main road: cells 0 to 5, then the exit. Side cell 6 joins before cell 2, side cell 7 joins before cell 4.
2. **Assumed numbers.** Free speed 60 km/h, backward wave speed 20 km/h, jam density 150 vehicles per km. These give a capacity of 2250 vehicles per hour, and each cell holds at most 37.5 vehicles.
3. **Flow rule (cell transmission model).** A cell can send only what it holds and receive only what it has room for. The flow between two cells is the smaller of the two. On red the flow is zero.
4. **Queues.** Arrivals that do not fit wait in a queue at the entrance. No vehicle is lost.
5. **Time step.** 5 seconds. In one step a vehicle moves 83 m, less than one cell. This is the CFL stability condition.
6. **Agents.** One at each junction. The *fixed* agent follows a timetable: 40 s main green, 5 s all-red, 40 s side green, 5 s all-red. The *responsive* agent computes a pressure for each approach (vehicles on the approach minus vehicles just after the junction) and switches to the busier approach, with at least 20 s and at most 60 s of green.
7. **Experiment.** Four demand patterns, five seeds, two kinds of agent: 40 runs. Both kinds get exactly the same arriving traffic in each case.

**Numbers.** Total vehicle-minutes on the road, fixed against responsive: balanced 3,263 and 2,213; main-road peak 10,851 and 2,840; side-road peak 6,435 and 3,174; exit limit 14,309 and 6,004. The responsive agents were better in all 20 cases. Vehicle count balanced to within 0.000000000003 vehicles.

**One update worked by hand.** Cell 1 holds 10 vehicles, which is 40 per km, so it can send 2250 per hour. Cell 2 holds 30 vehicles, which is 120 per km, so it can receive only 20 x (150 - 120) = 600 per hour. On green the flow is 600 per hour, which is 600 x 5 / 3600 = 0.83 vehicles in one step.

**Likely questions.**

- *What does LWR stand for?* Lighthill, Whitham and Richards. Their model treats traffic like a fluid in which vehicles are conserved.
- *Why can a cell hold a fraction of a vehicle?* The model works with density, not individual cars.
- *Why is the gap between the two agents so large?* The fixed timetable gives the main road green for 40 of every 90 seconds, so at most 2250 x 40 / 90 = 1000 vehicles per hour can pass. The main-road peak sends 1100. The fixed plan is overloaded and its queue keeps growing. A better-timed fixed plan would be much closer.
- *Is this multi-agent reinforcement learning?* No. Both agents are hand-written rules. Nothing is trained.
- *Do the agents talk to each other?* No. They affect each other only through the traffic between them.
- *Do the forecasts control the signals?* No. The two parts are separate.
- *Is this Los Angeles traffic?* No. The road, the parameters and the demand are invented.
- *What is spillback?* When a cell is full, the cell before it cannot send, so the queue grows backwards.

## 6. Results to know by heart

Test error in mph. Lower is better.

| Method | MAE 15 min | MAE 30 min | MAE 60 min |
| --- | --- | --- | --- |
| Persistence | 3.482 | 4.173 | 5.321 |
| Historical average | 4.187 | 4.187 | 4.187 |
| Random Forest | 2.972 | 3.423 | 3.896 |
| XGBoost | 2.920 | 3.376 | 3.874 |
| Temporal GRU | 3.119 | 3.811 | 4.929 |
| GRU + GAT | 3.099 | 3.780 | 4.881 |

Ablations at 60 minutes, seed 42: full model 4.877, self-loop only 4.923, uniform neighbours 4.891, no dropout 4.847.

Three-seed means at 60 minutes: GRU + GAT 4.881, self-loop only 4.931, temporal GRU 4.929.

## 7. The literature review, reference by reference

The numbers match the reference list in the report. For each one: what it is, why we cite it, and one sentence to say.

1. **Cho et al., 2014, "Learning phrase representations using RNN encoder-decoder".** The paper that introduced the GRU, for machine translation. We use a GRU to read each sensor's history. *Say:* "The GRU comes from Cho and colleagues; it is a recurrent unit with a reset gate and an update gate."
2. **Velickovic et al., 2018, "Graph attention networks".** Introduced attention on graphs: a node weighs its neighbours with learned weights. Our neighbour layer follows this design. *Say:* "Our graph layer is a graph attention layer in the style of Velickovic and colleagues."
3. **Li et al., 2018, "Diffusion convolutional recurrent neural network" (DCRNN).** A well-known traffic forecasting model that released the METR-LA dataset and its road graph. We use the dataset and the graph. Our model is much smaller and is not DCRNN. *Say:* "The dataset and the sensor graph come from the DCRNN paper."
4. **Lighthill and Whitham, 1955, "On kinematic waves II".** The first half of the LWR theory: traffic as a fluid with conserved vehicles. *Say:* "This is the L and W of LWR."
5. **Richards, 1956, "Shock waves on the highway".** The same idea, found independently. *Say:* "This is the R of LWR."
6. **Daganzo, 1994, "The cell transmission model".** Turns the LWR theory into a simple computation on road cells with sending and receiving limits. *Say:* "Our simulation is a cell transmission model, which is LWR computed cell by cell."
7. **Patire et al., 2015, "Technical overview of the cell transmission model" (Berkeley PATH).** A short practical description of the update rule. We implemented the update from this document. *Say:* "This is the description we actually coded from."
8. **Lioris and Varaiya, 2013, "Variants of max pressure control".** Max-pressure control: each junction serves the approach with the largest pressure, using local measurements only. Our responsive agent uses a simplified version. *Say:* "Our responsive rule is inspired by max pressure, but it is a simple heuristic and we claim none of the paper's guarantees."
9. **Kingma and Ba, 2015, "Adam".** The optimiser that updates the network's weights. *Say:* "Adam adapts the step size for each weight."
10. **Srivastava et al., 2014, "Dropout".** Randomly switching off values during training to reduce over-fitting. *Say:* "We use dropout of 0.1."
11. **Pascanu, Mikolov and Bengio, 2013, "On the difficulty of training recurrent neural networks".** Explains exploding gradients and proposes gradient clipping. *Say:* "This is why we clip the gradient norm at 5."
12. **Breiman, 2001, "Random forests".** The Random Forest method, one of our Phase 1 baselines.
13. **Chen and Guestrin, 2016, "XGBoost".** The gradient-boosted tree method, our best Phase 1 model and the one the networks are compared with.
14. **PyTorch documentation for `torch.nn.GRU`.** The exact form of the GRU equations in the library we used.

How to summarise the review in two sentences: "We took the time model from the GRU paper, the neighbour layer from the graph attention paper, and the dataset and graph from the DCRNN paper. For the simulation we took the theory from Lighthill, Whitham and Richards, the computation from Daganzo's cell transmission model, and the signal idea from max-pressure control."

All 14 references were checked against arXiv, Crossref or the publisher pages. That confirms they are real and correctly cited. It does not mean each of us has read each paper, so read at least the abstract of the ones in your module.

## 8. Questions any of us may get

- **What is the difference between Phase 1 and Phase 2?** Phase 1 used machine learning: one tree model per sensor on hand-made features. Phase 2 uses deep learning: one neural network for all sensors that learns its own features and can use the road graph.
- **What is your main finding?** Neighbours help a small network by about 1% at 60 minutes, but the per-sensor tree models from Phase 1 are still better.
- **Is that a failure?** It is an honest result. The experiment was designed to answer a question, and it did. A negative result that is measured carefully is still a result.
- **How do you know the gain is from neighbours?** The self-loop model has the same size and training, with only the neighbours removed, and it is worse in all three seeds.
- **Is the gain statistically significant?** We did not run a significance test. Three seeds show the spread between training runs.
- **Why does error grow with the horizon?** The further ahead, the less the current readings tell you.
- **What would you do next?** Tell the network which sensor it is looking at, give it a longer history, tune it more, and test on a period nobody has seen.
- **How are the two parts of the project connected?** Both are about connected roads. They are separate experiments: the forecasts do not control the signals.
- **Did you use AI tools?** Yes. See section 10.

## 9. What we must not claim

- That deep learning beat the Phase 1 models. It did not.
- A hybrid improvement. The best blend is XGBoost alone.
- A clean final test score. The test period was inspected in Phase 1.
- That the simulation is calibrated to Los Angeles, or that it shows real-world savings.
- That the agents are trained, or that this is multi-agent reinforcement learning.
- That the forecasts drive the signals.
- That attention weights prove how congestion spreads.
- That the faculty has accepted the scope. No project-specific brief beyond the general course instructions was available.

## 10. Being honest about how the work was made

The Phase 2 code, experiments and saved results were prepared under Kavya's coordination with substantial AI assistance, on top of the teammate prototype and the Phase 1 work. Each member integrated and reviewed one module through a pull request. This report, the deck and this guide were drafted with AI assistance from the saved results.

If asked, say exactly that, and then show what you understand: explain your module, trace one example by hand, and run its checks.

## 11. Things you can run

```bash
# all automated tests
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 pytest -q

# the simulation: 40 runs in about two seconds, no dataset needed
PYTHONPATH=src python scripts/run_control.py --run-dir results/runs/control-demo

# rebuild the report's tables and figures from the saved results
python report/phase2/make_assets.py
```

Forecasting with a saved network needs the trained model files, which are not in Git. The steps are in `docs/PHASE2_RUNBOOK.md`.

`docs/PHASE2_PRESENTATION_GUIDE.md` describes the earlier six-slide deck. Use this guide for the current 13-slide deck.
