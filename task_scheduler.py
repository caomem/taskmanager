#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  task_scheduler.py -- a script for task management and scheduling
#
#  Copyright (C) 2024 Guilherme Philippi <guilherme.philippi@hotmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sqlite3
from datetime import datetime, timedelta
from enum import Enum
import logging
import os

class Priority(Enum):
    """
    Enum to represent the priority of a task.
    """
    LOW = 1
    """
    Indicates low priority.
    """
    MEDIUM = 2
    """
    Indicates medium priority.
    """
    HIGH = 3
    """
    Indicates high priority.
    """

class TaskStatus(Enum):
    """
    Enum to represent the status of a task.
    """
    PENDING = 0
    """
    Indicates that the task is pending and has not been started.
    """
    PARTIALLY_COMPLETED = 1
    """
    Indicates that the task has been partially completed.
    """
    COMPLETED = 2
    """
    Indicates that the task has been completed.
    """
    CANCELLED = 3
    """
    Indicates that the task has been canceled.
    """

    def symbol(self):
        """
        Return a symbol representing the status of the task.
        """
        if self == TaskStatus.PENDING:
            return "[ ]"
        elif self == TaskStatus.PARTIALLY_COMPLETED:
            return "[/]"
        elif self == TaskStatus.COMPLETED:
            return "[X]"
        elif self == TaskStatus.CANCELLED:
            return "[ ]"
class Task:
    """
    Class to represent a task.
    """
    def __init__(self, name, priority=Priority.LOW, estimated_time=0, deadline=None, status=TaskStatus.PENDING):
        """
        Initialize a Task object.

        Args:
            name (str): The name of the task.
            priority (Priority, optional): The priority of the task. Defaults to Priority.LOW.
            estimated_time (int, optional): The estimated time required to complete the task (in hours). Defaults to 0.
            deadline (str, optional): The deadline of the task in the format 'YYYY-MM-DD'. Defaults to None.
            status (TaskStatus, optional): The status of the task. Defaults to TaskStatus.PENDING.
        """
        self.name = name
        self.priority = priority
        self.estimated_time = estimated_time
        self.deadline = deadline
        self.status = status

    def __str__(self):
        """
        Return a string representation of the task. It uses the MarkDown list format.
        """
        return f"1. {'~~' if self.status is TaskStatus.CANCELLED else ''}{self.status.symbol()} {self.name} ({self.priority.name}) Estimated Time: {self.estimated_time} hours [Deadline: {self.deadline}] {'~~' if self.status is TaskStatus.CANCELLED else ''}"

class TaskScheduler:
    """
    Class to manage tasks and scheduling.
    """
    def __init__(self, db_name, log_file='task_manager.log'):
        """
        Initialize a TaskScheduler object.

        Args:
            db_name (str): The name of the SQLite database file.
            log_file (str, optional): The name of the log file. Defaults to 'task_manager.log'.
        """
        self.conn = sqlite3.connect(db_name)
        self.log_file = log_file
        self.setup_logging()
        self.create_table()

    def setup_logging(self):
        """
        Setup logging configuration.
        """
        logging.basicConfig(filename=self.log_file, level=logging.ERROR)

    def log_error(self, error_message):
        """
        Log an error message.

        Args:
            error_message (str): The error message to log.
        """
        logging.error(error_message)

    def create_table(self):
        """
        Create the tasks table in the database.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                priority INTEGER NOT NULL,
                                estimated_time INTEGER NOT NULL,
                                deadline TEXT,
                                status INTEGER NOT NULL
                            )''')
            self.conn.commit()
        except sqlite3.Error as e:
            error_message = "Error creating tasks table: {}".format(e)
            self.log_error(error_message)
            raise Exception(error_message)

    def add_task(self, task):
        """
        Add a task to the database.

        Args:
            task (Task): The task to add to the database.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO tasks (name, priority, estimated_time, deadline, status) 
                              VALUES (?, ?, ?, ?, ?)''', (task.name, task.priority.value, task.estimated_time, task.deadline, task.status.value))
            self.conn.commit()
        except sqlite3.Error as e:
            error_message = "Error adding task: {}".format(e)
            self.log_error(error_message)
            raise Exception(error_message)

    def update_task(self, task_id, task):
        """
        Update a task in the database.

        Args:
            task_id (int): The ID of the task to update.
            task (Task): The updated task object.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''UPDATE tasks SET name=?, priority=?, estimated_time=?, deadline=?, status=? WHERE id=?''',
                           (task.name, task.priority.value, task.estimated_time, task.deadline, task.status.value, task_id))
            self.conn.commit()
        except sqlite3.Error as e:
            error_message = "Error updating task: {}".format(e)
            self.log_error(error_message)
            raise Exception(error_message)

    def get_tasks(self, include_completed=False):
        """
        Retrieve tasks from the database.

        Args:
            include_completed (bool, optional): Whether to include completed tasks. Defaults to False.

        Returns:
            list: A list of Task objects representing the tasks in the database.
        """
        try:
            cursor = self.conn.cursor()
            if include_completed:
                cursor.execute('''SELECT * FROM tasks''')
            else:
                cursor.execute('''SELECT * FROM tasks WHERE status = ? OR status = ?''', (TaskStatus.PENDING.value,TaskStatus.PARTIALLY_COMPLETED.value))
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                task = Task(row[1], Priority(row[2]), row[3], row[4], TaskStatus(row[5]))
                tasks.append(task)
            return tasks
        except sqlite3.Error as e:
            error_message = "Error retrieving tasks: {}".format(e)
            self.log_error(error_message)
            return None

    def get_task_by_id(self, task_id):
        """Get task by ID."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT * FROM tasks WHERE id=?''', (task_id,))
            row = cursor.fetchone()
            if row:
                return Task(row[1], Priority(row[2]), row[3], row[4], TaskStatus(row[5]))
            else:
                return None
        except sqlite3.Error as e:
            error_message = "Error retrieving tasks: {}".format(e)
            self.log_error(error_message)
            return None

    def get_task_ids_by_partial_name(self, partial_name):
        """
        Retrieve task IDs that match a partial name.

        Args:
            partial_name (str): The partial name to search for.

        Returns:
            list: A list of task IDs.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT id FROM tasks WHERE name LIKE ?''', ('%' + partial_name + '%',))
            rows = cursor.fetchall()
            task_ids = [row[0] for row in rows]
            return task_ids
        except sqlite3.Error as e:
            error_message = "Error retrieving task IDs by partial name: {}".format(e)
            self.log_error(error_message)
            return None

    def create_daily_task_list(self, total_time):
        """
        Create a daily task list based on the available time.

        Args:
            total_time (int): The total available time for tasks (in hours).

        Returns:
            list: A list of Task objects representing the daily task list.
        """
        try:
            daily_task_list = []
            remaining_time = total_time
            today = datetime.now().strftime('%Y-%m-%d')

            tasks_for_today = [task for task in self.get_tasks() if task.deadline == today and task.status != TaskStatus.COMPLETED]
            tasks_for_today.sort(key=lambda x: x.priority.value, reverse=True)

            for task in tasks_for_today:
                if task.estimated_time <= remaining_time:
                    daily_task_list.append(task)
                    remaining_time -= task.estimated_time

            if remaining_time <= 0:
                return daily_task_list

            remaining_tasks = [task for task in self.get_tasks() if task.deadline != today and task.status != TaskStatus.COMPLETED]
            remaining_tasks.sort(key=lambda x: (x.priority.value, x.deadline), reverse=True)

            for task in remaining_tasks:
                if task.estimated_time <= remaining_time:
                    daily_task_list.append(task)
                    remaining_time -= task.estimated_time
                    if remaining_time <= 0:
                        break
                    
            return daily_task_list
        except Exception as e:
            error_message = "Error creating daily task list: {}".format(e)
            self.log_error(error_message)
            return None

    def complete_task(self, task_id, partial_completion=False):
        """
        Mark a task as completed.

        Args:
            task_id (int): The ID of the task to mark as completed.
            partial_completion (bool, optional): Whether the task should be marked as partially completed. Defaults to False.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''UPDATE tasks SET status=? WHERE id=?''', (TaskStatus.PARTIALLY_COMPLETED.value if partial_completion else TaskStatus.COMPLETED.value, task_id))
            self.conn.commit()
        except sqlite3.Error as e:
            error_message = "Error completing task: {}".format(e)
            self.log_error(error_message)
            return False
    
    def cancel_task(self, task_id):
        """
        Mark a task as canceled.

        Args:
            task_id (int): The ID of the task to mark as completed.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''UPDATE tasks SET status=? WHERE id=?''', (TaskStatus.CANCELLED.value, task_id))
            self.conn.commit()
        except sqlite3.Error as e:
            error_message = "Error canceling task: {}".format(e)
            self.log_error(error_message)
            return False

    def notify_upcoming_tasks(self, days=1):
        """
        Retrieve tasks with deadlines within a specified number of days.

        Args:
            days (int, optional): The number of days to look ahead for upcoming tasks. Defaults to 1.

        Returns:
            list: A list of Task objects representing upcoming tasks.
        """
        try:
            upcoming_tasks = [task for task in self.get_tasks() if task.deadline is not None
                              and datetime.strptime(task.deadline, '%Y-%m-%d') <= datetime.now() + timedelta(days=days)]
            return upcoming_tasks
        except Exception as e:
            error_message = "Error notifying upcoming tasks: {}".format(e)
            self.log_error(error_message)
            return None

    def delete_task(self, task_id):
        """
        Deletes a task from the database.

        Args:
            task_id (int): The ID of the task to be deleted.

        Raises:
            sqlite3.Error: If an error occurs while accessing the database.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''DELETE FROM tasks WHERE id=?''', (task_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            error_message = "Error deleting task: {}".format(e)    
            self.log_error(error_message)
            return False