from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create stored procedures in the database'

    def handle(self, *args, **kwargs):
        self.create_task_by_user_procedure()
        self.get_tasks_by_user_procedure()
        self.get_tasks_by_status_procedure()
        self.get_tasks_by_due_date_procedure()
        self.get_tasks_by_status_and_date_procedure()
        self.update_tasks_by_user_procedure()
        self.delete_tasks_by_user_procedure()
        self.stdout.write(self.style.SUCCESS('Stored procedures created successfully'))


    def create_task_by_user_procedure(self):
        create_tasks_by_user = """
        CREATE PROCEDURE CreateTask
            @id NVARCHAR(32),
            @title NVARCHAR(255),
            @description NVARCHAR(MAX),
            @due_date DATETIMEOFFSET,
            @status NVARCHAR(30),
            @user_id CHAR(32)
        AS
        BEGIN
            INSERT INTO TaskApp_tasks (id, title, description, due_date, status, user_id)
            VALUES (@id, @title, @description, @due_date, @status, @user_id);
        END;
        """
        with connection.cursor() as cursor:
            cursor.execute(create_tasks_by_user)


    def get_tasks_by_user_procedure(self):
        get_tasks_by_user = """
        CREATE PROCEDURE GetTasksByUser
            @user_id CHAR(36)
        AS
        BEGIN
            SELECT * FROM TaskApp_tasks WHERE user_id = @user_id;
        END;
        """
        with connection.cursor() as cursor:
            cursor.execute(get_tasks_by_user)

    def get_tasks_by_status_procedure(self):
        tasks_by_status = """
        CREATE PROCEDURE GetTasksByStatus
            @user_id CHAR(36),
            @status VARCHAR(50)
        AS
        BEGIN
            SELECT * 
            FROM TaskApp_tasks 
            WHERE user_id = @user_id
            AND status = @status;
        END;
        """
        with connection.cursor() as cursor:
            cursor.execute(tasks_by_status)

    def get_tasks_by_due_date_procedure(self):
        tasks_by_due_date = """
           CREATE PROCEDURE GetTasksByDueDate
               @user_id CHAR(36),
               @due_date DATE = NULL
           AS
           BEGIN
               SELECT * 
               FROM TaskApp_tasks 
               WHERE user_id = @user_id
               AND due_date = @due_date;
           END;
           """
        with connection.cursor() as cursor:
            cursor.execute(tasks_by_due_date)

    def get_tasks_by_status_and_date_procedure(self):
        tasks_by_status_and_date = """
           CREATE PROCEDURE GetTasksByStatusAndDueDate
               @user_id CHAR(36),
               @status VARCHAR(50) = NULL,
               @due_date DATE = NULL
           AS
           BEGIN
               SELECT * 
               FROM TaskApp_tasks 
               WHERE user_id = @user_id
               AND status = @status
               AND due_date = @due_date;
               
           END;
           """
        with connection.cursor() as cursor:
            cursor.execute(tasks_by_status_and_date)

    def update_tasks_by_user_procedure(self):
        update_by_user = """
        CREATE PROCEDURE UpdateTask
            @task_id CHAR(36),
            @status VARCHAR(50) = NULL,
            @due_date DATE = NULL,
            @title VARCHAR(255) = NULL,
            @description TEXT = NULL
        AS
        BEGIN
            UPDATE TaskApp_tasks
            SET 
              status = COALESCE(@status, status),
              due_date = COALESCE(@due_date, due_date),
              title = COALESCE(@title, title),
              description = COALESCE(@description, description)
            WHERE id = @task_id;
        END;
        """
        with connection.cursor() as cursor:
            cursor.execute(update_by_user)

    def delete_tasks_by_user_procedure(self):
        delete_tasks_by_user = """
        CREATE PROCEDURE DeleteTask
            @task_id CHAR(36)
        AS
        BEGIN
            DELETE FROM TaskApp_tasks
            WHERE id = @task_id;
        END;
        """
        with connection.cursor() as cursor:
            cursor.execute(delete_tasks_by_user)
