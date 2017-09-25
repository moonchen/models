tesla <- read.csv('dataset.processed.csv')

library(ggplot2)
tesla$year <- factor(tesla$year)
ggplot(tesla, aes(miles, price, color=year)) + geom_point() + geom_smooth(method = lm, se = FALSE)
ggplot(tesla, aes(miles, price, color=year, size=battery, shape=factor(awd))) + geom_point() + scale_color_discrete('year') + scale_size('battery size', range=c(0.5,3)) + scale_shape_manual('AWD', values=c(1,16))
ggplot(tesla, aes(miles, price, color=factor(performance))) + geom_point() + geom_smooth(method = lm, se = FALSE)
ggplot(tesla, aes(miles, price, color=factor(awd))) + geom_point() + geom_smooth(method = lm, se = FALSE)


ggplot(tesla, aes(miles, price, color=battery)) + geom_point() + scale_color_continuous('battery') + facet_grid(. ~ year)


options("scipen"=100, "digits"=4)
m <- lm(price ~ year * miles + performance + awd + battery, tesla)
