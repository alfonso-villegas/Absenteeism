library(fBasics)
library(forecast)

data<-read.csv("Datos CO2.csv",header=TRUE,sep=",")
y<-data[,"CO2"][1:600]

ts.plot(y)
par(mfrow=c(2,1))


nlags=60
acf(y,nlags)
pacf(y,nlags)

#as we can see we have non-stationarity in the mean and probably stationarity in the variance
ndiffs(y, alpha=0.05, test=c("adf")) # regular differences

z <- diff(y)

ts.plot(z)
par(mfrow=c(2,1))
acf(z,nlags)
pacf(z,nlags)

# FIRST MODEL
s=12 
fit<-arima(y,order=c(1,1,0),seasonal=list(order=c(0,1,1),period=s)) 
fit

ts.plot(fit$residuals)

par(mfrow=c(2,1))
acf(fit$residuals,nlags)
pacf(fit$residuals,nlags)

Box.test(fit$residuals,lag=30) #WN
shapiro.test(fit$residuals) # Residuals are Normal, we have SWN

#no more differences needed
ndiffs(fit$residuals, alpha=0.05, test=c("adf"))
par(mfrow=c(1,1))
hist(fit$residuals,prob=T,ylim=c(0,7),xlim=c(mean(fit$residuals)-3*sd(fit$residuals),mean(fit$residuals)+3*sd(fit$residuals)),col="red")
lines(density(fit$residuals),lwd=2)
mu<-mean(fit$residuals)
sigma<-sd(fit$residuals)
x<-seq(mu-3*sigma,mu+3*sigma,length=100)
yy<-dnorm(x,mu,sigma)
lines(x,yy,lwd=2,col="blue")

#ci ar(1)
ci_low <- fit$coef[1] - 1.96 * 0.0398
ci_high <- fit$coef[1] + 1.96 * 0.0398
print(c(ci_low,ci_high))
#SIGNIFICANT

#ci sma(1)
ci_low <- fit$coef[2] - 1.96 * 0.0203
ci_high <- fit$coef[2] + 1.96 * 0.0203
print(c(ci_low,ci_high))
#SIGNIFICANT

# FORECASTING
w.pred<-predict(fit,n.ahead=132)
predictions1<-w.pred$pred

ts.plot(predictions1)

# Comparing  real values with the predictions
real<-data[,"CO2"][601:732]
c=1:132
par(mfrow=c(1,1))
par(mar=c(3,3,1,1))
plot(c,predictions1,type="b",col="blue")
lines(c,real,col="orange",type="b")
legend("topleft",c("real","forecast"),
       col = c("orange","blue"),pch = c(1,1),bty ="n" )

# point predictions and standard errors

y.pred<-predict(fit,n.ahead=132)
y.pred$pred   # point predictions
y.pred$se    # standard errors

# plotting real data with point predictions
new <- c(y,y.pred$pred) # real data + predicted values

plot.ts(new,main="Predictions",
        ylab="Dollars",col=3,lwd=2) # time series plot
lines(y,col=4,lwd=2) # for the second series
legend("topleft",legend=c("Predictions","Historical"),col=c(3,4),
       bty="n",lwd=2)

# SECOND MODEL
s=12 
fit2<-arima(y,order=c(4,1,0),seasonal=list(order=c(0,1,1),period=s)) 
fit2

ts.plot(fit2$residuals)

par(mfrow=c(2,1))
acf(fit2$residuals,nlags)
pacf(fit2$residuals,nlags)

Box.test(fit2$residuals,lag=30) #WN
shapiro.test(fit2$residuals) # Normality, there SWN

#no more differences needed
ndiffs(fit2$residuals, alpha=0.05, test=c("adf"))
par(mfrow=c(1,1))
hist(fit2$residuals,prob=T,ylim=c(0,7),xlim=c(mean(fit$residuals)-3*sd(fit$residuals),mean(fit$residuals)+3*sd(fit$residuals)),col="red")
lines(density(fit2$residuals),lwd=2)
mu<-mean(fit2$residuals)
sigma<-sd(fit2$residuals)
x<-seq(mu-3*sigma,mu+3*sigma,length=100)
yy<-dnorm(x,mu,sigma)
lines(x,yy,lwd=2,col="blue")

#ci ar(1)
ci_low <- fit2$coef[1] - 1.96 * 0.0420
ci_high <- fit2$coef[1] + 1.96 * 0.0420
print(c(ci_low,ci_high))
#SIGNIFICANT

#ci ar(2)
ci_low <- fit2$coef[2] - 1.96 * 0.0446
ci_high <- fit2$coef[2] + 1.96 * 0.0446
print(c(ci_low,ci_high))
#SIGNIFICANT

#ci ar(3)
ci_low <- fit2$coef[3] - 1.96 * 0.0441
ci_high <- fit2$coef[3] + 1.96 * 0.0441
print(c(ci_low,ci_high))
#SIGNIFICANT

#ci ar(4)
ci_low <- fit2$coef[4] - 1.96 * 0.0414
ci_high <- fit2$coef[4] + 1.96 * 0.0414
print(c(ci_low,ci_high))
#SIGNIFICANT

#ci sma(1)
ci_low <- fit2$coef[5] - 1.96 * 0.0214
ci_high <- fit2$coef[5] + 1.96 * 0.0214
print(c(ci_low,ci_high))
#SIGNIFICANT

# FORECASTING
w.pred<-predict(fit2,n.ahead=132)
predictions2<-w.pred$pred

ts.plot(predictions2)

# Comparing the real values with the predicted ones
real<-data[,"CO2"][601:732] 
c=1:132
par(mfrow=c(1,1))
par(mar=c(3,3,1,1))
plot(c,predictions2,type="b",col="blue")
lines(c,real,col="orange",type="b")
legend("topleft",c("real","forecast"),
       col = c("orange","blue"),pch = c(1,1),bty ="n" )

# point predictions and standard errors

y.pred<-predict(fit2,n.ahead=132)
y.pred$pred   # point predictions
y.pred$se    # standard errors

# plotting real data with point predictions
new <- c(y,y.pred$pred) # real data + predicted values

plot.ts(new,main="Predictions",
        ylab="Dollars",col=3,lwd=2) # time series plot
lines(y,col=4,lwd=2) # for the second series
legend("topleft",legend=c("Predictions","Historical"),col=c(3,4),
       bty="n",lwd=2)


# Models performance:
install.packages("MLmetrics")
library(MLmetrics)
MAPE(y_pred = predictions1,y_true = real) #MAPE model 1 = 0.42%
MAPE(y_pred = predictions2,y_true = real) #MAPE model 2 = 0.39%
