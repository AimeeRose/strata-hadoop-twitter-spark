library(shiny)
library(ggplot2)

titles <- read.csv('data/strata-titles-to-watch.csv', stringsAsFactors = FALSE)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  output$distPlot <- renderPlot({
    titles$Title <- factor(titles$Title, levels = titles$Title[order(-titles$TweetCount)])

    ggplot(titles, aes(x = Title, y = TweetCount)) +
      geom_bar(stat = "identity", fill = "#56B4E9") +
      coord_flip() +
      ylab('Number of Tweets') +
      xlab('Session Title')
  }, height = 700)
})
