install.packages(c(
    ###################################
    # DATA MANIPULATION & PROCESSING
    ###################################
    # Core Data Tools
    "tidyverse",      # meta-package (dplyr, tidyr, ggplot2, readr, purrr)
    "data.table",     # fast data operations
    "dtplyr",         # data.table/dplyr bridge
    "janitor",        # data cleaning
    "vroom",          # fast file reading
    "arrow",          # large dataset handling
    "bit64",          # better integer support
    "fst",            # fast serialization
    "disk.frame",     # out-of-memory data manipulation
    
    ###################################
    # STATISTICS & MACHINE LEARNING
    ###################################
    # General Statistics
    "car",            # companion to applied regression
    "lme4",           # mixed effects models
    "nlme",           # nonlinear mixed effects
    "survival",       # survival analysis
    "sandwich",       # robust statistics
    "broom",          # tidy model outputs
    "stargazer",      # statistical tables
    "emmeans",        # estimated marginal means
    "multcomp",       # multiple comparisons
    "boot",           # bootstrapping
    "MASS",           # modern statistics
    "nnet",           # neural networks
    "mgcv",           # GAMs
    "lmerTest",       # tests for mixed models
    
    # Machine Learning
    "MLmetrics",      # evaluation metrics
    "caret",          # ML training framework
    "randomForest",   # random forest models
    "xgboost",        # gradient boosting
    "e1071",          # SVM, Naive Bayes
    "glmnet",         # regularized regression
    "tidymodels",     # unified ML workflow
    "recipes",        # feature engineering
    "tensorflow",     # deep learning backend
    "keras",          # deep learning
    "h2o",            # automated ML
    "lightgbm",       # light gradient boosting
    "ranger",         # fast random forest
    
    ###################################
    # NETWORK SCIENCE & GRAPH ANALYSIS
    ###################################
    "igraph",         # network analysis and visualization
    "network",        # network objects handling
    "sna",            # social network analysis
    "statnet",        # statistical analysis of networks
    "tidygraph",      # tidy network manipulation
    "ggraph",         # grammar of graph visualization
    "graphlayouts",   # graph layout algorithms
    "netrankr",       # network centrality
    "sand",           # statistical analysis of network data
    "netdiffuseR",    # network diffusion
    "ergm",           # exponential random graph models
    "networkDynamic", # dynamic network analysis
    "ndtv",           # network dynamic temporal visualization
    "backbone",       # network backbone extraction
    
    ###################################
    # VISUALIZATION
    ###################################
    # Static Plotting
    "ggpubr",         # publication ready plots
    "gridExtra",      # arrange multiple plots
    "viridis",        # color palettes
    "GGally",         # ggplot2 extensions
    "corrplot",       # correlation plots
    "ggridges",       # ridgeline plots
    "ggrepel",        # text label repulsion
    "patchwork",      # plot composition
    "cowplot",        # publication quality plots
    "waffle",         # waffle charts
    "treemapify",     # treemaps
    "ggforce",        # extended ggplot2
    "rayshader",      # 3D visualization
    "rgl",            # 3D visualization
    "plotROC",        # ROC curves
    "DiagrammeR",     # diagram creation
    "esquisse",       # interactive ggplot2 builder
    "ggiraph",        # interactive ggplot
    "ggstatsplot",    # statistical visualization
    "ggthemes",       # additional themes
    "ggsci",          # scientific journal themes
    "ggtext",         # improved text rendering
    "ggExtra",        # marginal plots
    
    # Interactive Visualization
    "plotly",         # interactive plots
    "leaflet",        # interactive maps
    "gganimate",      # animated visualizations
    "DT",             # interactive tables
    "gt",             # grammar of tables
    "rbokeh",         # Bokeh plots
    "highcharter",    # Highcharts plots
    "networkD3",      # network visualization
    "visNetwork",     # interactive networks
    "threejs",        # 3D scatterplots
    
    ###################################
    # ADVANCED ANALYTICS
    ###################################
    # Dimensionality Reduction
    "Rtsne",          # t-SNE implementation
    "umap",           # UMAP dimensionality reduction
    "isomap",         # isometric feature mapping
    
    # Clustering
    "dbscan",         # density-based clustering
    "mclust",         # model-based clustering
    "cluster",        # clustering algorithms
    "factoextra",     # clustering visualization
    "dendextend",     # dendrogram manipulation
    "NbClust",        # determining optimal clusters
    
    # Optimization
    "ROI",            # R optimization infrastructure
    "ompr",           # optimization modeling
    "nloptr",         # nonlinear optimization
    "optimx",         # optimization methods
    
    ###################################
    # TIME SERIES
    ###################################
    "forecast",       # time series forecasting
    "xts",            # extended time series
    "zoo",            # time series objects
    "tsibble",        # tidy time series
    "prophet",        # Facebook's forecasting
    "timetk",         # time series toolkit
    "tibbletime",     # time-aware tibbles
    "anomalize",      # time series anomaly detection
    
    ###################################
    # SPATIAL DATA
    ###################################
    "sf",             # simple features
    "sp",             # spatial data
    "raster",         # raster data
    "rgdal",          # geospatial data
    "rgeos",          # geometry operations
    "mapview",        # interactive viewing
    
    ###################################
    # EXPLAINABLE AI & MODEL INTERPRETATION
    ###################################
    "DALEX",          # model explanation
    "iml",            # interpretable machine learning
    "lime",           # local interpretable model-agnostic explanations
    "shapviz",        # SHAP value visualization
    "pdp",            # partial dependence plots
    "vip",            # variable importance plots
    
    ###################################
    # ANOMALY DETECTION & QUALITY CONTROL
    ###################################
    "anomalize",      # time series anomaly detection
    "qcc",            # quality control charts
    "AnomalyDetection", # Twitter's anomaly detection
    "mvoutlier",      # multivariate outlier detection
    
    ###################################
    # ENSEMBLE METHODS & STACKING
    ###################################
    "caretEnsemble",  # ensemble methods for caret
    "SuperLearner",   # super learning/stacking
    "subsemble",      # subsemble learning
    "stacks",         # stacking models
    
    ###################################
    # DEVELOPMENT & DOCUMENTATION
    ###################################
    "devtools",       # package development
    "roxygen2",       # documentation
    "testthat",       # unit testing
    "knitr",          # report generation
    "rmarkdown",      # R markdown
    "bookdown",       # book authoring
    "flexdashboard",  # dashboard creation
    "shiny",          # web applications
    "shinydashboard", # dashboard framework
    "plumber",        # API creation
    "profvis",        # profiling tools
    "drake",          # data pipeline tool
    "workflowr",      # reproducible research
    "checkpoint",     # package version management
    "packrat",        # project dependency management
    "groundhog",      # reproducible package management
    "tarchetypes",    # pipeline patterns
    
    ###################################
    # DATA IMPORT & WEB
    ###################################
    "httr",           # HTTP requests
    "rvest",          # web scraping
    "jsonlite",       # JSON handling
    "readxl",         # Excel files
    "writexl",        # write Excel files
    "haven",          # SPSS/SAS/Stata files
    "xml2",           # XML processing
    "RCurl",          # web retrieval
    "RSQLite",        # SQLite interface
    "RMySQL",         # MySQL interface
    "RPostgres",      # PostgreSQL interface
    
    ###################################
    # PERFORMANCE & PARALLEL PROCESSING
    ###################################
    "parallel",       # base parallel processing
    "foreach",        # parallel loops
    "doParallel",     # parallel backend
    "future",         # parallel processing
    "furrr",          # parallel purrr
    "promises",       # async programming
    
    ###################################
    # TEXT MINING & NLP
    ###################################
    "tidytext",       # text mining
    "quanteda",       # text analysis
    "text2vec",       # text vectorization
    "topicmodels",    # topic modeling
    "wordcloud2",     # word clouds
    "tokenizers",     # text tokenization
    
    ###################################
    # UTILITIES
    ###################################
    "lubridate",      # date-time handling
    "scales",         # visualization scaling
    "stringi",        # string manipulation
    "chk",            # input validation
    "RcppProgress",   # progress bars
    "rlemon",         # optimization
    "skimr",          # summary statistics
    "fs",             # file system operations
    "here",           # file paths
    "config",         # configuration
    "logger",         # logging
    "memoise",        # memoization
    "cachem",         # caching
    "pins",           # pin resources
    "targets",        # pipeline toolkit
    "renv"            # dependency management
), 
repos = "http://cran.us.r-project.org",
dependencies = TRUE
)