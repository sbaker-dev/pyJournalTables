webuse census2.dta, clear

* Basic regression
reg drate medage marriage i.region

* Basic regression with clustering
reg drate medage marriage i.region, cluster(region)

* Summary table
sum drate medage marriage region i.region

* Tab table
tab region

* Reghdfe with absorbed degrees of freedom
reghdfe drate medage marriage, absorb(i.region)

* Reghdfe with absorbed degrees of freedom with clustering
reghdfe drate medage marriage, absorb(i.region) cluster(region)




