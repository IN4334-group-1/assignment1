
library(pls)


linear.loop <- function(model, data, runs=10) {
	results = c();

	for (i in 1:runs) {
		sample.train <- sample(nrow(data), size = 0.5 * nrow(data))
	    train.data <- data[sample.train,]
	    test.data <- data[-sample.train,]

	    linearModel <- lm(model, data=train.data, na.action=na.omit)
		linearModel$xlevels[["country_code"]] <- union(linearModel$xlevels[["country_code"]], levels(ds$country_code))
		linearModel$xlevels[["language"]] <- union(linearModel$xlevels[["language"]], levels(ds$language))
		linearModel$xlevels[["domains"]] <- union(linearModel$xlevels[["language"]], levels(ds$domains))

		linearPrediction <- predict(linearModel, newdata=test.data, na.action=na.omit)

		predictions.lm.ds <- as.data.frame(linearPrediction)
		predictions.lm.ds$index <- as.numeric(rownames(predictions.lm.ds))
		predictions.lm.ds <- predictions.lm.ds[with(predictions.lm.ds, order(index)),]

		testDataMean <- mean(test.data[rownames(predictions.lm.ds),]$stars) #predictions.lm.ds is een dataframe met resultaten
		SSTot <- sum((test.data[rownames(predictions.lm.ds),]$stars - testDataMean)^2) 
		SSRes <- sum((test.data[rownames(predictions.lm.ds),]$stars - predictions.lm.ds$linearPrediction)^2)
		results[i] <- (1 - SSRes/SSTot) 
	}
	results
}

pcr.loop <- function(model, data, runs=10) {

	results = c()

	for (i in 1:runs) {
		sample.train <- sample(nrow(data), size = 0.5 * nrow(data))
	    train.data <- data[sample.train,]
	    test.data <- data[-sample.train,]

	    pcrModel <- pcr(model, data=train.data, na.action = na.omit)
		pcrModel$xlevels[["country_code"]] <- union(pcrModel$xlevels[["country_code"]], levels(ds$country_code))
		pcrModel$xlevels[["language"]] <- union(pcrModel$xlevels[["language"]], levels(ds$language))
		pcrModel$xlevels[["domains"]] <- union(pcrModel$xlevels[["language"]], levels(ds$domains))

		pcrPrediction <- predict(pcrModel, newdata=test.data, ncomp=50, na.action = na.omit)

		predictions.pcr.ds <- as.data.frame(pcrPrediction)
		predictions.pcr.ds$index <- as.numeric(rownames(predictions.pcr.ds))
		predictions.pcr.ds <- predictions.pcr.ds[with(predictions.pcr.ds, order(index)),]

		testDataMean <- mean(test.data[rownames(predictions.pcr.ds),]$stars) #predictions.lm.ds is een dataframe met resultaten
		SSTot <- sum((test.data[rownames(predictions.pcr.ds),]$stars - testDataMean)^2) 
		SSRes <- sum((test.data[rownames(predictions.pcr.ds),]$stars - predictions.pcr.ds$`stars.50 comps`)^2)
		results[i] <- (1 - SSRes/SSTot)
	}
	results
}