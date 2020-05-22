# Roadmap

1. **Experimental Framework** - Build a framework to support the scientific method. Proposing hypothesis, making changes, and measuring the results. ANC is particularly sensitive to input parameters and little work has been put in to determine optimal results
2. **Optimizations** - Currently the system sees frequent underflow errors which translates to not enough data is being provided to the output speaker. This likely indicates issues with the performance of the system
3. **Add support for multiple reference microphones** - It is assumed that the system could perform better with additional microphones supporting the ANC processing system
4. **Refactor to generic libraries to support open source community** - This was not the original intent of Diminish, but there is a lack of available libraries for this type of application