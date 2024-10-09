QUERY_FREE_CLASSROOMS="""
    SELECT c.room_number, 
           b.name AS building_name,
           MIN(CASE 
                 WHEN co.start_time > CURTIME() AND co.day_of_week = DAYNAME(CURDATE()) 
                 THEN co.start_time 
               END) AS next_lecture_time
    FROM classrooms c
    JOIN buildings b ON c.building_id = b.id
    LEFT JOIN schedules s ON c.id = s.classroom_id
    LEFT JOIN courses co ON s.course_id = co.id
    WHERE (co.start_time IS NULL
           OR (CURTIME() NOT BETWEEN co.start_time AND co.end_time)
           OR (co.day_of_week != DAYNAME(CURDATE())))
    GROUP BY c.room_number, b.name;
    """