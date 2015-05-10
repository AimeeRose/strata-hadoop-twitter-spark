library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Strata + Hadoop Session Popularity by Number of Tweets"),
  
  # Sidebar with a slider input for the number of bins
  sidebarLayout(
    sidebarPanel(
      p("This bar plot represents the twitter popularity of the Strata + Hadoop conference sessions."),
      p("Using tweets with the #StrataHadoop hashtag since May 5, 2015, 
        a tweet was categorized as likely relating to a given session 
        if the text of the tweet bore a third of the same words as the session title. 
        Sessions with less than 45 tweets were filtered out."),
      p("There are problems with this approach but it achieved the desired objective,
        which was to determine which sessions I should watch when videos become available."),
      width = 3),
    
    # Show a plot of the generated distribution
    mainPanel(plotOutput("distPlot"), width = 9))
))