# Research Goal

To build an NFL draft model capable of producing meaningful player predictions.  I plan to do so using a Random Forest trained on NFL Combine and Pro Day physical measurements, individual and team college statistics, and engineered features.  Player performance is impacted by round and team selection in the draft - first-round selections receive more opportunities than seventh-round selections, different schemes fit some players better.  Because of this it's also important to include some regression to publicly available consensus draft rankings.

# Model Output

I've decided to take the novel approach of using player ratings from EA Sports' Madden video game franchise as a proxy for player production, skill, and value.  This is beneficial for a number of reasons.  The first is that these ratings provide continuous output on a consistent scale across both years and positions; a player rated 99 overall is considered to be elite at their position, regardless of the unique responsibilities or challenges in quantifying performance specific to that position.  The second reason is that Madden ratings predate modern quantitative evaluative metrics like those provided by Football Outsiders or Pro Football Focus. 

Madden ratings explained - https://fivethirtyeight.com/features/madden/#

Overall ratings are calculated using position-specific formulas that weight individual attributes like speed, strength, and tackling.  Ratings are updated each year through a Bayesian-like process of weighing new information to update old.  To aggregate ratings for each player, I use a 5-part mean which includes ratings in Years 1-4 and Peak rating. 

NFL rookie contract length is 4 seasons (along with a fifth year club option for first-round picks), while the average career length in the NFL is less than 4 years.  As such, when building a draft model is makes sense to only consider production accrued during the first 4 years of a player's career.

Year 1 represents the Madden rating given to each player following their rookie season.  For this reason, the final year for which complete data is available is the 2014 draft class (with Madden 19 providing Year 4 ratings).  This decision was made to better capture NFL success, as rookie player ratings are highly dependent on draft order.  For example, in Madden 2008 rookie #1 overall pick JaMarcus Russell was awarded an overall rating of 82, just 1 point lower than #3 overall pick Joe Thomas.  The next year, Russell's rating was 83, while Thomas was a 97 overall.  By Madden 2010, Russell was given a rating of 72 overall, while Thomas maintained his 97 overall rating.  Year 3 and Year 4 ratings have been given double weight for the same reason, with the added effect of lowering the ratings of players who were not able to stay in the league for at least 4 years.

While this metric on the whole does a good job of ranking player talent and production, it is blind to players who peaked later in their careers or those who had short careers.  Notable examples of each include Eric Weddle (84.6 rating, eventual 2x All Pro, 6x Pro Bowl) and Jon Beason (95.4 rating, 1x All-Pro, 3x Pro Bowl).  Weddle did not reach his peak until after re-signing with the Chargers as an unrestricted free agent prior to the 2011 season, and could have presumably reached his peak while playing for another team.  Beason suffered an Achilles injury during the 2011 season and eventually lost his job with the Panthers, starting in only 26 games in the years following his rating window.  Beason would have been eligible to sign as a free agent following the 2011 season had the Panthers not offered a contract extension.  

In the NFL, the drafting team maintains the exclusive right to employ each player for 4 years following their selection, thus it is incumbent upon the team to select and develop players who provide the most value during that period.  For that reason I stand by the decision to evaluate draft selections only on a player's first 4 years in the league.  

# Dataset

The dataset covers the 2006-2014 draft classes and includes players who were ranked in NFL Draft Scout's top 300 in their draft year.  I have removed all quarterbacks, kickers, punters, long snappers, and fullbacks due to the relatively small sample sizes or extreme specialization that each position requires.  It might be valuable to evaluate these positions later – particularly quarterbacks – but for now the model focuses exclusively on 13 "skill" positions, bucketed into 7 position groups.

The dataset restrictions exclude some notable players ranked outside of the top 300, both drafted and undrafted, who went on to varying degrees of success in the NFL.  At the top extreme are 4-time All Pro Antonio Brown and Super Bowl LIII MVP Julian Edelman.  But while many players on this list never played a down in the NFL, it is important to be aware of which players are excluded and it may be worthwhile to expand the dataset in the future.

I have removed players from the dataset whose NFL careers were cut prematurely short either voluntarily or involuntarily (due to injury, not ability).  These players' ratings (or lack thereof) are not representative of their production and thus only serve to complicate the dataset and confuse any modeling attempts.  Examples include Aaron Hernandez, Gaines Adams, and Chris Borland.

There is also a subset of players who drastically changed position upon entering the league.  This is contrary to less extreme position changes (tackle to guard, cornerback to safety), which occur frequently.  These players have been removed because their college statistics create noisy data.  Examples: Denard Robinson, Devin Hester, J.R. Sweezy.

# College Statistics

College statistics have been collected and cleaned at the FBS level from Sports Reference.  Using college statistics is important because they provide information on a player's in-game performance.  However, college football styles vary greatly among teams and have changed over time.  Therefore we must control for differences in pace and style of play when considering college numbers.  Rather than attempt to fit a model on raw season total statistics, I've decided to use neutralized per game statistics under the following parameters:

-	Receiving statistics have been normalized to 30 team pass attempts per game
-	Rushing statistics have been normalized to 35 team rush attempts per game
-	Sacks/Interceptions/Passes Defended normalized to 30 opponent pass attempts per game
-	Tackles/TFL/Fumbles normalized to 65 opponent offensive plays per game
-	Regression to position-specific mean as function of percentage of team games played 

To illustrate this point let's look at Calvin Johnson and Michael Crabtree, who were both highly productive college wide receivers selected early in the first round.

-	Calvin Johnson, Georgia Tech (2006): 14 G, 76 catches, 1202 yards, 15 TD
-	Michael Crabtree, Texas Tech (2008): 13 G, 97 catches, 1165 yards, 19 TD

The two statlines appear very similar without context.  It's easy to make this distinction empirically, but little effort has been made to translate college statistics into more informative data.  Johnson and Crabtree put up similar overall numbers, but Crabtree did it in an air raid style offense that relied heavily on passing while Johnson played on a more balanced offense.

-	Georgia Tech (2006): 368 total team pass attempts (26 per game)
-	Texas Tech (2008): 662 total team pass attempts (51 per game)

When we neutralize both players' statistics, we can better compare each player's level of production.

-	Calvin Johnson (neutralized): 6.2 catches, 97.6 yards, 1.2 TD
-	Michael Crabtree (neutralized): 4.4 catches, 52.8 yards, 0.9 TD

Compare those numbers to each player's NFL career statistics:

-	Calvin Johnson (NFL per game): 5.4 catches, 86.1 yards, 0.6 TD
-	Michael Crabtree (NFL per game): 4.5 catches, 53.0 yards, 0.4 TD

This is a cherry-picked example but it does well to show that while raw statistics are not to be trusted, college data when put into the proper context can be made more predictive.  On a larger scale, we can compare RMSE of the model when including raw college statistics compared to pace- and schedule-neutralized statistics.  Controlling for strength of schedule does not improve the predictiveness of the model, but controlling for pace and style of play does have a significant effect.

| Neutralization | RMSE |
| :---: | :---: |
| Raw per Game | 8.065 |
| Pace-Neutralized per Game | 8.029 |
| Pace- and Schedule-Neutralized per Game | 8.058 |


# NFL Combine and Pro Day Measurements

The final major inputs of the draft model are the physical measurements taken at the NFL Combine and university Pro Days.  Pro Day measurements are harder to come by due to their decentralized and often scarcely reported nature.  Fortunately, NFL Draft Scout has maintained a database of reported Pro Day measurements spanning the years in our dataset.

There is an enormous benefit in using Pro Day measurements in a model like this.  It allows for a larger training set by including data on players who were not invited to the NFL Combine, but also provides much more complete data because not all players who attend the combine perform the full slate of workouts.  This lessens the need for imputation and reduces uncertainty.

However, there is bias observed in Pro Day measurements.  Pro Days are typically scheduled in the weeks following the NFL Combine, giving players more time to train for the specific physical events.  Furthermore, they often take place at the players' home campuses in environments in which the players feel more comfortable.  Lastly, many events (most notably the 40-yard dash) are hand-timed at Pro Days, leading to better reported times than the electronic times at the Combine.  Each of these factors contributes to improvement in every event among the population of players who participated both at the NFL Combine and at their university Pro Day.

**Players who participated in both NFL Combine and Pro Day**

| Measurement |	Combine |	Pro Day |	n |	Sigma |	Adjustment |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 40 Yard Dash |	4.80 |	4.70 |	831 |	0.076	| + 0.07 |
| 20 Yard Split |	2.79 |	2.71 |	733 |	0.065	| + 0.06 |
| 10 Yard Split	| 1.68 |	1.62 |	739 |	0.057	| + 0.04 |
| Bench Press |	20.0 reps |	21.7 reps |	254 |	2.556	| - 1.2 |
| Vertical Jump |	31.7" |	33.6"	| 593	| 2.342	| - 1.3" |
| Broad Jump |	112.9" |	115.2" |	481	| 4.356	| - 1.6" |
| 20 Yard Shuttle |	4.46	| 4.42 |	424	| 0.155	| + 0.03 |
| 3 Cone Drill |	7.34 |	7.22 |	342	| 0.223	| + 0.08 |

In order to correct for this bias, I've (somewhat arbitrarily) chosen to shift recorded Pro Day measurements by 70% of the mean delta.  Even when we correct for some of the systematic bias observed in Pro Day measurements, we must also recognize that most physical measurements aren't static.  Some players aren't performing at maximum physical capacity on the day of the Combine<sup>1</sup>, occasionally players injure themselves during their workout<sup>2</sup>, and the measurements aren't always recorded with perfect accuracy or consistency<sup>3</sup>.  

<sup>1</sup> https://www.cleveland.com/osu/2018/03/ohio_state_defensive_end_tyqua_1.html

<sup>2</sup> https://www.washingtontimes.com/news/2019/mar/3/dexter-lawrence-clemson-prospect-injures-hamstring/

<sup>3</sup> https://www.zybeksports.com/hand-timed-versus-electronic-timed-40-yard-dash/

A dataset with this much uncertainty lends itself well to fuzzy set theory.  In simple terms, this will allow us to consider not only a player's recorded 40 yard time of 4.40, but will also consider some probability that their "true" speed is 4.39 or 4.43.  So when the model attempts to predict NFL success given a player's 40 yard dash time, it's not based on a singular number but rather a distribution of times centered around that number.

Fuzzy Set Theory explanation - https://www.doc.ic.ac.uk/~nd/surprise_96/journal/vol4/sbaa/report.fuzzysets.html






