# NFL-draft-research

NFL rookie contract length is 4 seasons (along with a fifth year club option for first-round picks), while the average career length in the NFL is less than 4 years.  As such, when building a draft model is makes sense to only consider production accrued during the first 4 years of a player's career.

I've decided to take the novel approach of using player ratings from EA Sports' Madden video game franchise as a proxy for player production, skill, and value during a player's first 4 years in the league.  This is beneficial for a number of reasons.  The first is that these ratings provide continuous output on a consistent scale across both years and positions; a player rated 99 overall is considered to be elite at their position, regardless of the unique responsibilities or challenges in quantifying performance specific to that position.  The second reason is that Madden ratings predate modern quantitative evaluative metrics like those provided by Football Outsiders or Pro Football Focus.  

Madden ratings explained - https://fivethirtyeight.com/features/madden/#

Overall ratings are calculated using position-specific formulas that weight individual attributes like speed, strength, and tackling.  Ratings are updated each year through a Bayesian-like process of weighing new information to update old.  To aggregate ratings for each player, I use a 5-part mean which includes ratings in Years 1-4 and Peak rating. 

Year 1 represents the Madden rating given to each player following their rookie season.  For this reason, the final year for which complete data is available is the 2014 draft class (with Madden 19 providing Year 4 ratings).  This decision was made to better capture NFL success, as rookie player ratings are highly dependent on draft order.  For example, in Madden 2008 rookie #1 overall pick JaMarcus Russell was awarded an overall rating of 82, just 1 point lower than #3 overall pick Joe Thomas.  The next year, Russell's rating was 83, while Thomas was a 97 overall.  By Madden 2010, Russell was given a rating of 72 overall, while Thomas maintained his 97 overall rating.  Year 3 and Year 4 ratings have been given double weight for the same reason, with the added effect of lowering the ratings of players who were not able to stay in the league for at least 4 years.

While this metric on the whole does a good job of ranking player talent and production, it is blind to players who peaked later in their careers or those who had short careers.  Notable examples of each include Eric Weddle (84.6 rating, eventual 2x All Pro, 6x Pro Bowl) and Jon Beason (95.4 rating, 1x All-Pro, 3x Pro Bowl).  Weddle did not reach his peak until after re-signing with the Chargers as an unrestricted free agent prior to the 2011 season, and could have presumably reached his peak while playing for another team.  Beason suffered an Achilles injury during the 2011 season and eventually lost his job with the Panthers, starting in only 26 games in the years following his rating window.  Beason would have been eligible to sign as a free agent following the 2011 season had the Panthers not offered a contract extension.  

In the NFL, the drafting team maintains the exclusive right to employ each player for 4 years following their selection, thus it is incumbent upon the team to select and develop players who provide the most value during that period.  For that reason I stand by the decision to evaluate draft selections only on a player's first 4 years in the league.  

The dataset covers the 2006-2014 draft classes and includes players who were ranked in NFL Draft Scout's top 300 in their draft year.  I have removed all quarterbacks, kickers, punters, long snappers, and fullbacks due to the relatively small sample sizes or extreme specialization that each position requires.  It might be valuable to evaluate these positions later – particularly quarterbacks – but for now the model focuses exclusively on the following 13 positions, bucketed into 7 position groups.

The dataset restrictions exclude some notable players, both drafted and undrafted, who went on to varying degrees of success in the NFL.  At the top extreme are Antonio Brown, 4-time All Pro, and Julian Edelman, Super Bowl LIII MVP.  But while many players on this list never played a down in the NFL, it is important to be aware of which players are excluded and it may be worthwhile to expand the dataset in the future.

I have removed players from the dataset whose NFL careers were cut prematurely short either voluntarily or involuntarily (due to injury, not ability).  These players' ratings (or lack thereof) are not representative of their production and thus only serve to complicate the dataset and confuse any modeling attempts.

There is also a subset of players who drastically changed position upon entering the league.  This is contrary to less extreme position changes (tackle to guard, cornerback to safety), which occur frequently.  These players have been removed because their college statistics create noisy data.









