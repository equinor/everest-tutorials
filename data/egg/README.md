# `egg`


## Description of the Egg case

The Egg Model[^1] is a synthetic reservoir model consisting of an ensemble of 100 three-dimensional permeability realizations of a channelized reservoir produced under water flooding conditions with eight water injectors and four producers. 
The dataset[^2] is made available by J.D. Jansen and TUDelft using the _General Terms_ of _4TU.Centre for Research Data_ license terms.

![The first 10 realizations of the Egg ensemble.](./docs/source/assets/ensemble_10.png)


## Content of the project

The case consists of:

1. a templated reservoir simulator `EGG_MODEL_FLOW.DATA` and a templated schedule `SCHEDULE_TEMPLATE` designed for use with the flow reservoir simulator[^3].
2. an EVEREST configuration file `egg.yml` and input optimization templates and configuration files. 

The organization of these files follows an informal standard with two top level directories, `everest` and `flow`, each with its own relevant sub-directories to include supporting files. 
This is the current layout of the files:


```
egg
├── 4TU.Centre for Research Data - General terms of use.pdf  # complete license terms for the EGG dataset
├── COPYING.md                                               # plain-text link to license terms for the EGG dataset
├── README.md                                                # this documentation
├── everest
│   ├── input
│   │   ├── files
│   │   │   ├── injection_rate_contraints.yml                # well phase, rate and time constraints
│   │   │   ├── prices.yml                                   # model financial assumptions 
│   │   │   ├── template_config.yml                          # schedule template configuration
│   │   │   └── wells_readydate.json                         # well parameters with available start date 
│   │   └── templates
│   │       └── wconinje.jinja                               # schedule template
│   └── model
│       └── egg.yml                                          # EGG case EVEREST configuration
└── flow
    ├── include
    │   └── ACTIVE.INC                                       # active grid cells in the reservoir simulation model
    ├── model
    │   ├── EGG_MODEL_FLOW.DATA                              # templated reservoir simulation case for flow
    │   └── SCHEDULE_TEMPLATE.SCH                            # templated schedule for flow
    └── realizations
        └── realization-[0-99]                               # model realizations folders (e.g. realization-13)
            └── PERM.INC                                     # realization-dependent permeability
```


## The available Egg dataset

There is no intention to reproduce the results of the original Egg dataset[^2]. 
The dataset is only used as an input to the optimization experiments.
So the obtained drainage strategy is expected to differ from previous publications.  


## Modifications to the original datasets

There are deviations from the original dataset that were needed to implement the optimization experiments. 
Most of these changes are related to the reservoir simulator `DATA` file.
These changes are summarized below:

- Replaced the `mDarcy.INC` by `PERM.INC` (realization-dependent permeability).
- Removed `RPTONLY` from the `SUMMARY` section.
- Added `RPTRST` with `'BASIC=4' 'FREQ=2' 'ALLPROPS'`.
- Added `FOIP` and `FPR` to the `SUMMARY` section.
- Changed `START` to `24.03.2025`.
- Removed the `TUNNING` section.
- Renamed realization 100 to realization 0 to be consistent with EVEREST.



[^1]: Jansen, J.D., Fonseca, R.M., Kahrobaei, S., Siraj, M.M., Van Essen, G.M. and Van den Hof, P.M.J. (2014), The egg model – a geological ensemble for reservoir simulation. Geosci. Data J., 1: 192-195. https://doi.org/10.1002/gdj3.21
[^2]: J.D.Jansen (2013): The Egg Model - data files. Version 1. 4TU.ResearchData. dataset. https://doi.org/10.4121/uuid:916c86cd-3558-4672-829a-105c62985ab2
[^3]: https://opm-project.org/?page_id=19
