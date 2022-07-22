# Generated by Django 4.0.6 on 2022-07-22 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Тип для передачи в функцию _intersect_schedule
                CREATE TYPE dataset as (
                    username    varchar,
                    user_ranges tstzrange
                );
                
                -- Рекурсивно рассчитывает пересечения для конкретных наборов
                CREATE OR REPLACE FUNCTION _intersect_schedule(_table dataset[]) RETURNS tstzrange[] AS
                $$
                DECLARE
                    min_username varchar;
                    time_row     tstzrange;
                    time_subrow  tstzrange;
                    intersection tstzrange;
                    subresult    tstzrange[];
                    result       tstzrange[];
                BEGIN
                    min_username := (SELECT username FROM unnest(_table) limit  1);
                    IF NOT EXISTS(SELECT * FROM unnest(_table) WHERE username <> min_username) THEN
                        RETURN array(select user_ranges FROM unnest(_table));
                    END IF;
                
                    FOR time_row IN (SELECT user_ranges FROM unnest(_table) WHERE username = min_username) LOOP
                        subresult := _intersect_schedule(
                            array(SELECT ROW(username, user_ranges)::dataset FROM unnest(_table) WHERE username > min_username)
                        );
                        FOR time_subrow IN SELECT unnest(subresult) LOOP
                            intersection := time_row * time_subrow;
                            IF NOT isempty(intersection) THEN
                                result := array_append(result, intersection);
                            END IF;
                        END LOOP;
                    END LOOP;
                
                    RETURN result;
                END;
                $$ LANGUAGE plpgsql;
                
                -- Рассчитывает расписания по имени ссылки
                CREATE OR REPLACE FUNCTION calculate_shedule(meeting_name varchar) RETURNS tstzrange[] AS
                $$
                BEGIN
                    RETURN _intersect_schedule(array(
                            SELECT ROW (username, user_ranges)::dataset
                            FROM calendarapp_userdatarange
                            WHERE meeting_id_id = (SELECT id FROM calendarapp_meeting WHERE name = meeting_name)
                            GROUP BY username, user_ranges
                            ORDER BY count(username), username
                        ));
                END;
                $$ LANGUAGE plpgsql;
            """,
            reverse_sql="""
                DROP FUNCTION calculate_shedule(varchar);
                DROP FUNCTION _intersect_schedule(dataset[]);
                DROP TYPE dataset;
            """
        )
    ]
