import pytest
import functools

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


# Static helpers for common operations:
class Project:

    @staticmethod
    async def create(name=f"Project {create_timestamp()}", language='Py'):
        output_model = await validate_models(
            mcp, 'create_project', {'name': name, 'language': language},
            ProjectListResponse
        )
        return output_model.projects[0]

    @staticmethod
    async def read(id_):
        output_model = await validate_models(
            mcp, 'read_project', {'projectId': id_}, ProjectListResponse
        )
        return output_model.projects[0]

    @staticmethod
    async def update(id_, **kwargs):
        await validate_models(
            mcp, 'update_project', {'projectId': id_} | kwargs, RestResponse
        )

    @staticmethod
    async def delete(id_):
        await validate_models(
            mcp, 'delete_project', {'projectId': id_}, RestResponse
        )

    @staticmethod
    async def list_():
        output_model = await validate_models(
            mcp, 'list_projects', output_class=ProjectListResponse
        )
        return output_model.projects


# Test suite:
class TestProject:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_create_project(self, language):
        name = f"Project {create_timestamp()}"
        project = await Project.create(name, language)
        # Test if the name and language are correct.
        assert project.name == name
        assert project.language.value == language
        # Delete the project to clean up.
        await Project.delete(project.projectId)

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
    async def test_create_project_with_request_validation_errors(self, args):
        await raises_validation_error(
            'create_project', args, CreateProjectRequest
        )

    @pytest.mark.asyncio
    async def test_read_project(self):
        # Create a project.
        name = f"Project {create_timestamp()}"
        language = 'Py'
        id_ = (await Project.create(name, language)).projectId
        # Read the project.
        project = await Project.read(id_)
        # Test if the name and language are correct.
        assert project.name == name
        assert project.language.value == language
        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    async def test_read_project_with_invalid_args(self):
        # Try to read a project that doesn't exist.
        await validate_models(
            mcp, 'read_project', {'projectId': -1}, 
            ReadProjectRequest, False
        )

    @pytest.mark.asyncio
    async def test_update_project(self):
        # Create a project.
        id_ = (await Project.create()).projectId
        
        # Update the project name.
        new_name = f"Project {create_timestamp()}"
        await Project.update(id_, name=new_name)
        # Test if the new name is correct.
        project = await Project.read(id_)
        assert project.name == new_name
        
        # Update the project description.
        new_description = f"Description {create_timestamp()}"
        await Project.update(id_, description=new_description)
        # Test if the new description is correct.
        project = await Project.read(id_)
        assert project.description == new_description
        
        # Update the project name and description.
        new_name = f"Project {create_timestamp()}"
        new_description = f"Description {create_timestamp()}"
        await Project.update(
            id_, name=new_name, description=new_description
        )
        # Test if the new name & description are correct.
        project = await Project.read(id_)
        assert project.name == new_name
        assert project.description == new_description

        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    async def test_update_project_with_a_nonunique_name(self):
        # Create 2 projects.
        name_1 = f"Project {create_timestamp()}"
        id_1 = (await Project.create(name_1)).projectId
        name_2 = f"Project {create_timestamp()}"
        id_2 = (await Project.create(name_2)).projectId
        # Try updating the project names to match.
        await validate_models(
            mcp, 'update_project', {'projectId': id_2, 'name': name_1}, 
            UpdateProjectRequest, False
        )
        # Delete the projects.
        await Project.delete(id_1)
        await Project.delete(id_2)

    @pytest.mark.asyncio
    async def test_delete_projects_with_invalid_args(self):
        # Try to delete a project that doesn't exist.
        await validate_models(
            mcp, 'delete_project', {'projectId': -1}, 
            DeleteProjectRequest, False
        )

    @pytest.mark.asyncio
    async def test_list_projects(self):
        await Project.list_()
        
