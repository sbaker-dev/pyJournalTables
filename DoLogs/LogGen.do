webuse census2.dta, clear

log using "$LogDir/StataLog.log", replace
* Basic regression
reg drate medage marriage i.region

* Basic regression with clustering
reg drate medage marriage i.region, cluster(region)

* Panel setup
xtset region

* Panel Fixed effects
xtreg drate medage marriage, fe

* Panel Fixed effects with clustering
xtreg drate medage marriage, fe cluster(region)

* Panel Random effects with clustering
xtreg drate medage marriage, cluster(region)

* Reghdfe with absorbed degrees of freedom
reghdfe drate medage marriage, absorb(i.region)

* Reghdfe with absorbed degrees of freedom with clustering
reghdfe drate medage marriage, absorb(i.region) cluster(region)

* Mixed 
mixed drate medage marriage || region: medage marriage

* Generate a binary variable for probit / logit
gen regionN = region
gen north = 0
replace north = 1 if regionN == 1
replace north = 2 if regionN == 1

* Probit
probit north drate

* Logit
logit north drate

* Summary table
sum drate medage marriage region i.region

* Tab table
tab region

log close



* Multiple table per log check
log using "$LogDir/MultiTableLog.log", replace
reg drate medage 
reg drate medage marriage 
reg drate medage marriage i.region
log close
