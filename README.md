SQL to dump reviews:
```
select
       pr.PRODUCTREVIEWID as id,
       pr.PRODUCTID as product_id,
       pr.REVIEWTITLE as review_title,
       pr.REVIEWTEXT as review_text,
       pr.AVERAGERATING as average_rating
from WEB_PRODUCTREVIEW pr
         inner join (
    select pr.PRODUCTID, count(PRODUCTREVIEWID) as totalreviews
    from WEB_PRODUCTREVIEW pr
    where LANGUAGEID = 1
      and PRODUCTREVIEWSTATEID = 4
    group by PRODUCTID
    order by totalreviews desc
) as topreviews ON pr.PRODUCTID = topreviews.PRODUCTID
where totalreviews > 1000;
```
