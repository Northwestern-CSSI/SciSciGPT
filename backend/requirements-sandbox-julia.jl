import Pkg; Pkg.add("Plots")  # Main plotting library with multiple backends
import Pkg; Pkg.add("PlotlyJS")  # Interactive plotting with Plotly
import Pkg; Pkg.add("Gadfly")  # Grammar of graphics plotting library
import Pkg; Pkg.add("VegaLite")  # Declarative visualization library
import Pkg; Pkg.add("Makie")   # High-performance plotting library
import Pkg; Pkg.add("ColorSchemes")  # Color palette management
import Pkg; Pkg.add("Colors")     # Color manipulation
import Pkg; Pkg.add("ImageIO")    # Image file I/O
import Pkg; Pkg.add("ImageMagick")  # Image processing backend
import Pkg; Pkg.add("FileIO")     # Unified file I/O interface

# Install network visualization packages
import Pkg; Pkg.add("Graphs")  # Graph data structures and algorithms
import Pkg; Pkg.add("GraphRecipes")  # Graph plotting recipes for Plots
import Pkg; Pkg.add("NetworkLayout")  # Graph layout algorithms
import Pkg; Pkg.add("GraphPlot")  # Graph visualization library
import Pkg; Pkg.add("LightGraphs")  # Graph algorithms and data structures
import Pkg; Pkg.add("MetaGraphs")  # Graph with metadata support
import Pkg; Pkg.add("SimpleWeightedGraphs")  # Weighted graph support
import Pkg; Pkg.add("GraphDataFrameBridge")  # Bridge between Graphs and DataFrames

# Install data analysis and manipulation packages
import Pkg; Pkg.add("DataFrames")  # Tabular data manipulation
import Pkg; Pkg.add("CSV")      # CSV file reading/writing
import Pkg; Pkg.add("JSON3")    # JSON parsing and generation
import Pkg; Pkg.add("Statistics")  # Statistical functions
import Pkg; Pkg.add("Distributions")  # Probability distributions
import Pkg; Pkg.add("StatsBase")  # Basic statistics functions
import Pkg; Pkg.add("GLM")      # Generalized linear models
import Pkg; Pkg.add("Clustering")  # Clustering algorithms
import Pkg; Pkg.add("MultivariateStats")  # Multivariate statistics

# Install scientific computing packages
import Pkg; Pkg.add("LinearAlgebra")  # Linear algebra operations
import Pkg; Pkg.add("Random")     # Random number generation
import Pkg; Pkg.add("Dates")      # Date and time handling
import Pkg; Pkg.add("TimeSeries")  # Time series analysis
import Pkg; Pkg.add("Interpolations")  # Interpolation methods
import Pkg; Pkg.add("Optim")      # Optimization algorithms
import Pkg; Pkg.add("DifferentialEquations")  # Differential equation solvers

# Install machine learning packages
import Pkg; Pkg.add("MLJ")       # Machine learning framework
import Pkg; Pkg.add("Flux")      # Neural network framework
import Pkg; Pkg.add("ScikitLearn")  # Scikit-learn interface
import Pkg; Pkg.add("DecisionTree")  # Decision tree algorithms
import Pkg; Pkg.add("XGBoost")   # Gradient boosting framework
import Pkg; Pkg.add("LIBSVM")    # Support vector machines
import Pkg; Pkg.add("KernelFunctions")  # Kernel methods

# Install deep learning and AI packages
import Pkg; Pkg.add("Transformers")  # Transformer models
import Pkg; Pkg.add("TextAnalysis")  # Text processing and NLP
import Pkg; Pkg.add("WordTokenizers")  # Text tokenization
import Pkg; Pkg.add("Embeddings")  # Word embeddings
import Pkg; Pkg.add("BSON")       # Binary JSON for model serialization

# Install geospatial packages
import Pkg; Pkg.add("GeoInterface")  # Geospatial data interface
import Pkg; Pkg.add("Shapefile")  # Shapefile reading/writing
import Pkg; Pkg.add("GeoJSON")    # GeoJSON support
import Pkg; Pkg.add("Proj4")      # Coordinate transformations

# Install web and API packages
import Pkg; Pkg.add("HTTP")       # HTTP client/server
import Pkg; Pkg.add("WebSockets")  # WebSocket support
import Pkg; Pkg.add("Gumbo")      # HTML parsing
import Pkg; Pkg.add("Cascadia")   # CSS selectors
import Pkg; Pkg.add("Genie")      # Web framework

# Install development and testing packages
import Pkg; Pkg.add("Test")       # Unit testing framework
import Pkg; Pkg.add("BenchmarkTools")  # Performance benchmarking
import Pkg; Pkg.add("Profile")    # Code profiling
import Pkg; Pkg.add("Revise")     # Code reloading
import Pkg; Pkg.add("Debugger")   # Interactive debugging


x = 1
println(x + 2)



using Plots
using Statistics
x = randn(100)
y = 2x .+ randn(100) * 0.5
p1 = scatter(x, y, title="Sample Scatter Plot", xlabel="X values", ylabel="Y values", markersize=4, markercolor=:blue, legend=false)
plot!(p1, x, 2x, linewidth=2, linecolor=:red, label="Trend line")