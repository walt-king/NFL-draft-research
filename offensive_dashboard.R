library(fmsb)
library(png)
library(ggplot2)
library(grid)
library(gridExtra)
library(ggpubr)
library(cowplot)


pos <- "TE"
player <- "Rob Gronkowski"


combine <- read.csv('file_directory')
combine <- subset(combine, select = c("full_name","position","year","ht","wt","hand_size","arm_length"
                                ,"speed_score","vert_power","broad_power","quickness_score","adj_bench"
                                ,"catch_radius","adj_att","adj_ruyds","adj_rutd","adj_rec","adj_reyds"
                                ,"adj_retd","adj_scrim_yds","adj_off_td","non_off_td","off_usage"))

columns <- c("ht","wt","hand_size","arm_length","speed_score","vert_power"
            ,"broad_power","quickness_score","adj_bench","catch_radius")

perf_columns <- c("adj_att","adj_ruyds","adj_rutd","adj_rec","adj_reyds"
                 ,"adj_retd","adj_scrim_yds","adj_off_td","non_off_td","off_usage")

pos_subset <- subset(combine, position == pos)

for (column in columns)
{
  pos_subset[column]<-as.integer(100*rank(pos_subset[column])/nrow(pos_subset))
}

for (column in perf_columns)
{
  pos_subset[column]<-as.integer(100*rank(pos_subset[column])/length(pos_subset[column][!is.na(pos_subset[column])]))
}

## Radar Chart
plot_subset <- subset(pos_subset, full_name == player)
year <- plot_subset$year[1]
plot_subset <- rbind(rep(100,13), rep(0,13), plot_subset)
plot_subset <- plot_subset[4:13]
names(plot_subset) <- c("Height","Weight","Hand Size","Arm Length","Speed","Vert","Broad"
                       ,"Quickness","Bench","Catch Radius")

png('image_upload.png')

radarchart(plot_subset, axistype = 1
           ,pcol=rgb(0.2,0.5,0.5,0.9) , pfcol=rgb(0.2,0.5,0.5,0.5) , plwd=2
           ,cglcol="grey", cglty=1, axislabcol="grey", caxislabels=seq(0,100,25), cglwd=0.8
           #,title = paste(player, "-- ", pos, "/", year)
           ,title = "Physical Measurements", vlcex = 0.8)

dev.off()

radar_img <- readPNG('image_upload.png')

p1<-ggplot(data = plot_subset) + coord_fixed() + 
  annotation_custom(rasterGrob(radar_img
                               ,width = unit(1,"npc")
                               ,height = unit(1,"npc"))
                    ,-Inf, Inf, -Inf, Inf) +
  theme(plot.margin = margin(0,-1,-1,-1,"cm"))



## Performance Chart
bar_subset <- subset(pos_subset, full_name == player)
bar_subset <- bar_subset[14:23]
names(bar_subset) <- c("Att","Rush Yds","Rush TD","Rec","Rec Yds","Rec TD","Scrim Yds","Total TD"
                      ,"Return TD","Usage Rate")

bar_x <- names(bar_subset)
bar_y <- as.integer(bar_subset[1,])

bar_subset <- data.frame(bar_x = bar_x
                         ,bar_y = as.integer(bar_y))

bar_subset$bar_x <- factor(bar_subset$bar_x
                           ,levels = c("Att","Rush Yds","Rush TD","Rec","Rec Yds","Rec TD","Scrim Yds"
                                       ,"Total TD","Return TD","Usage Rate"))

png('image_upload.png')

ggplot(data=bar_subset, aes(x = bar_x, y = bar_y, fill = bar_y)) +
  geom_bar(stat="identity") + 
  ylim(0,100) + 
  scale_fill_gradient2(low='red', mid='red', high='darkgreen', space='Lab'
                       ,breaks = c(0,10,20,30,40,50,60,70,80,90,100)
                       ,limit = c(0,100)) +
  theme(legend.position="none"
        ,axis.text=element_text(size=12)
        ,axis.text.x = element_text(angle = 70, hjust = 1)
        ,plot.title = element_text(size=17)) +
  labs(title = "College Performance", y = "Percentile", x = "") +
  #coord_fixed(0.5) +
  geom_segment(aes(x = 0.5, y = 50, xend = 10.5, yend = 50), data = bar_subset, linetype = 2) +
  geom_segment(aes(x = 0.5, y = 0, xend = 10.5, yend = 0), data = bar_subset) +
  geom_segment(aes(x = 0.5, y = 100, xend = 10.5, yend = 100), data = bar_subset, linetype = 2)

dev.off()

bar_img <- readPNG('image_upload.png')

p2<-ggplot(data = bar_subset) + coord_fixed() + 
  annotation_custom(rasterGrob(bar_img
                               ,width = unit(1,"npc")
                               ,height = unit(1,"npc"))
                    ,-Inf, Inf, -Inf, Inf)


title <- ggdraw() + draw_label(paste(player, "-- ", pos, "/", year), fontface='bold')

grid <- plot_grid(p1, p2)

plot_grid(title, grid, ncol = 1, rel_heights=c(0.1, 1))



