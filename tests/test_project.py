import pytest

from main import mcp
from utils import (
    validate_models, 
    raises_validation_error, 
    create_timestamp,
)
from models import (
    CreateProjectRequest,
    ReadProjectRequest, 
    UpdateProjectRequest,
    DeleteProjectRequest,
    ProjectListResponse,
    RestResponse,
)


class TestProject:

    # Static helpers for common operations:
    @staticmethod
    async def create(payload):
        output_model = await validate_models(
            mcp, 'create_project', payload, ProjectListResponse
        )
        return output_model.projects[0]

    @staticmethod
    async def read(payload):
        output_model = await validate_models(
            mcp, 'read_project', payload, ProjectListResponse
        )
        return output_model.projects[0]

    @staticmethod
    async def update(payload):
        await validate_models(mcp, 'update_project', payload, RestResponse)    

    @staticmethod
    async def delete(payload):
        await validate_models(mcp, 'delete_project', payload, RestResponse)

    @staticmethod
    async def list_():
        output_model = await validate_models(
            mcp, 'list_projects', output_class=ProjectListResponse
        )
        return output_model.projects

    # Test suite:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'args',
        [
            # Case 1: Python
            {'language': 'Py'},
            # Case 2: C#
            {'language': 'C#'},
        ]
    )
    async def test_create_project(self, args):
        name = f"Project {create_timestamp()}"
        language = args['language']
        project = await TestProject.create(
            {'name': name, 'language': language}
        )
        # Test if the name and language are correct.
        assert project.name == name
        assert project.language.value == language
        # Delete the project to clean up.
        await TestProject.delete({'projectId': project.projectId})

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'args',
        [
            # Case 1: Missing a required property (`language`)
            {'name': 'Test Project'},
            # Case 2: Invalid property value (`language`)
            {'name': 'Test Project', 'language': 'C++'},
        ]
    )
    async def test_create_project_with_invalid_args(self, args):
        await raises_validation_error(
            'create_project', args, CreateProjectRequest
        )

    @pytest.mark.asyncio
    async def test_read_project(self):
        # Create a project.
        name = f"Project {create_timestamp()}"
        language = 'Py'
        project = await TestProject.create(
            {'name': name, 'language': language}
        )
        # Read the project.
        args = {'projectId': project.projectId}
        project = await TestProject.read(args)
        # Test if the name and language are correct.
        assert project.name == name
        assert project.language.value == language
        # Delete the project to clean up.
        await TestProject.delete(args)

    @pytest.mark.asyncio
    async def test_read_project_with_invalid_args(self):
        # Try to read a project that doesn't exist.
        await raises_validation_error(
            'read_project', {'projectId': -1}, ReadProjectRequest
        )

    @pytest.mark.asyncio
    async def test_update_project(self):
        # Create a project.
        name = f"Project {create_timestamp()}"
        project = await TestProject.create({'name': name, 'language': 'Py'})
        args = {'projectId': project.projectId}
        
        # Update the project name.
        new_name = f"Project {create_timestamp()}"
        await TestProject.update(args | {'name': new_name})
        # Test if the new name is correct.
        project = await TestProject.read(args)
        assert project.name == new_name
        
        # Update the project description.
        new_description = f"Description {create_timestamp()}"
        await TestProject.update(args | {'description': new_description})
        # Test if the new description is correct.
        project = await TestProject.read(args)
        assert project.description == new_description
        
        # Update the project name and description.
        new_name = f"Project {create_timestamp()}"
        new_description = f"Description {create_timestamp()}"
        await TestProject.update(
            args | {'name': new_name, 'description': new_description}
        )
        # Test if the new name & description are correct.
        project = await TestProject.read(args)
        assert project.name == new_name
        assert project.description == new_description

        # Delete the project to clean up.
        await TestProject.delete(args)

    @pytest.mark.asyncio
    async def test_update_project_with_a_nonunique_name(self):
        language = 'Py'
        # Create project 1.
        name_1 = f"Project {create_timestamp()}"
        project_1 = await TestProject.create(
            {'name': name_1, 'language': language}
        )
        # Create project 2.
        name_2 = f"Project {create_timestamp()}"
        project_2 = await TestProject.create(
            {'name': name_2, 'language': language}
        )
        # Try updating the project names to match.
        await raises_validation_error(
            'update_project', 
            {'projectId': project_2.projectId, 'name': name_1}, 
            UpdateProjectRequest
        )
        # Delete the projects.
        await TestProject.delete({'projectId': project_1.projectId})
        await TestProject.delete({'projectId': project_2.projectId})

    @pytest.mark.asyncio
    async def test_list_projects(self):
        await TestProject.list_()
