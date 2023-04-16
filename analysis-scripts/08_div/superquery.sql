-- SQLite

SELECT r.repo_id, case when f1.file_id is null then 0 else 1 end f1_exists,
                    case when f2.file_id is null then 0 else 1 end f2_exists,
                    case when f3.file_id is null then 0 else 1 end f3_exists,
                    case when f4.file_id is null then 0 else 1 end f4_exists
    FROM repo r
        LEFT JOIN file f1 on f1.repo_id=r.repo_id join secret s on f1.file_id=s.file_id
        LEFT JOIN file f2 on f2.repo_id=r.repo_id join email e on f2.file_id=e.file_id
        LEFT JOIN file f3 on f3.repo_id=r.repo_id join privdata p on f3.file_id=p.file_id
        LEFT JOIN file f4 on f4.repo_id=r.repo_id join dependency d on f4.file_id=d.file_id
GROUP BY r.repo_id
LIMIT 50;

--select distinct f1.repo_id from file f1 on f1.repo_id=r.repo_id join secret s on f1.file_id=s.file_id