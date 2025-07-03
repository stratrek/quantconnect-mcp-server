import pytest
import os

from main import mcp
from test_project import Project
from utils import validate_models, send_request_with_invalid_args
from models import (
    CreateCollaboratorRequest,
    ReadCollaboratorsRequest,
    UpdateCollaboratorRequest,
    DeleteCollaboratorRequest,
    CreateCollaboratorResponse,
    ReadCollaboratorsResponse,
    UpdateCollaboratorResponse,
    DeleteCollaboratorResponse
)

COLLABORATOR_ID = os.getenv('QUANTCONNECT_COLLABORATOR_ID')


# Static helpers for common operations:
class ProjectCollaboration:

    @staticmethod
    async def create(
            project_id, collaborator_id, collaboration_live_control,
            collaboration_write):
        output_model = await validate_models(
            mcp, 'create_project_collaborator', 
            {
                'projectId': project_id,
                'collaboratorUserId': collaborator_id,
                'collaborationLiveControl': collaboration_live_control,
                'collaborationWrite': collaboration_write
            }, 
            CreateCollaboratorResponse
        )
        return output_model.collaborators

    @staticmethod
    async def read(project_id):
        output_model = await validate_models(
            mcp, 'read_project_collaborators', {'projectId': project_id}, 
            ReadCollaboratorsResponse
        )
        return output_model.collaborators

    @staticmethod
    async def update(project_id, collaborator_user_id, live_control, write):
        output_model = await validate_models(
            mcp, 'update_project_collaborator', 
            {
                'projectId': project_id,
                'collaboratorUserId': collaborator_user_id,
                'liveControl': live_control,
                'write': write
            }, 
            UpdateCollaboratorResponse
        )
        return output_model.collaborators

    @staticmethod
    async def delete(project_id, collaborator_id):
        output_model = await validate_models(
            mcp, 'delete_project_collaborator', 
            {'projectId': project_id, 'collaboratorId': collaborator_id}, 
            DeleteCollaboratorResponse
        )
        return output_model.collaborators


# Test suite:
class TestProjectCollaboration:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    @pytest.mark.parametrize('collaboration_live_control', [True, False])
    @pytest.mark.parametrize('collaboration_write', [True, False])
    async def test_create_project_collaboration(
            self, language, collaboration_live_control, collaboration_write):
        # Create a project.
        project_id = (await Project.create(language=language)).projectId
        # Add a collaborator.
        collaborators = await ProjectCollaboration.create(
            project_id, 
            COLLABORATOR_ID, 
            collaboration_live_control,
            collaboration_write
        )
        # Test if the collaborator was added.
        assert len(collaborators) == 2
        assert any(
            [c.publicId == COLLABORATOR_ID for c in collaborators]
        )
        # Test if the live control and write permissions are right.
        permission = 'write' if collaboration_write else 'read'
        for c in collaborators:
            if c.publicId == COLLABORATOR_ID:
                assert c.liveControl == collaboration_live_control
                assert c.permission.value == permission
        # Remove the collaborators and delete the project to clean up.
        await ProjectCollaboration.delete(project_id, COLLABORATOR_ID)
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_create_project_collaboration_with_invalid_args(self):
        # Create a project.
        project_id = (await Project.create()).projectId
        # Test the invalid requests.
        await send_request_with_invalid_args(
            mcp, 'create_project_collaborator', CreateCollaboratorRequest,
            {
                'projectId': project_id,
                'collaboratorUserId': COLLABORATOR_ID,
                'collaborationLiveControl': True,
                'collaborationWrite': True
            },
            [
                # Try to add a collaborator to a project that doesn't 
                # exist.
                {'projectId': -1},
                # Try to add a collaborator to a project using an 
                # invalid user Id for the collaborator.
                {'collaboratorUserId': ' '}
            ]
        )
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_read_project_collaboration(self):
        # Create a project.
        project_id = (await Project.create()).projectId
        # Add a collaborator.
        await ProjectCollaboration.create(
            project_id, COLLABORATOR_ID, True, True
        )
        # Read the collaborator information of this project.
        collaborators = await ProjectCollaboration.read(project_id)
        # Test if the collaborator was added.
        assert len(collaborators) == 2
        assert any(
           [c.publicId == COLLABORATOR_ID for c in collaborators]
        )
        # Remove the collaborators and delete the project to clean up.
        await ProjectCollaboration.delete(project_id, COLLABORATOR_ID)
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_read_project_collaboration_with_invalid_args(self):
        # Try to read the collaborator information for a project that 
        # doesn't exist.
        await validate_models(
            mcp, 'read_project_collaborators', {'projectId': -1}, 
            ReadCollaboratorsRequest, False
        )

    @pytest.mark.asyncio
    async def test_update_project_collaboration(self):
        # Create a project.
        project_id = (await Project.create()).projectId
        # Add a collaborator.
        await ProjectCollaboration.create(
            project_id, COLLABORATOR_ID, True, True
        )
        # Update the collaborator live control and write permissions.
        collaborators = await ProjectCollaboration.update(
            project_id, COLLABORATOR_ID, False, False
        )
        # Test if the update worked.
        assert len(collaborators) == 2
        for c in collaborators:
            if c.publicId == COLLABORATOR_ID:
                assert not c.liveControl
                assert c.permission.value == 'read'
        # Remove the collaborators and delete the project to clean up.
        await ProjectCollaboration.delete(project_id, COLLABORATOR_ID)
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_update_project_collaboration_with_invalid_args(self):
        # Create a project.
        project_id = (await Project.create()).projectId
        # Add a collaborator.
        await ProjectCollaboration.create(
            project_id, COLLABORATOR_ID, True, True
        )
        # Test the invalid requests.
        await send_request_with_invalid_args(
            mcp, 'update_project_collaborator', UpdateCollaboratorRequest,
            {
                'projectId': project_id,
                'collaboratorUserId': COLLABORATOR_ID,
                'liveControl': True,
                'write': True
            },
            [
                # Try to update a collaborator on a project that 
                # doesn't exist.
                {'projectId': -1},
                # Try to update a collaborator on a project using an 
                # invalid user Id for the collaborator.
                {'collaboratorUserId': ' '}
            ]
        )
        # Remove the collaborators and delete the project to clean up.
        await ProjectCollaboration.delete(project_id, COLLABORATOR_ID)
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_delete_project_collaboration_with_invalid_args(self):
        # Create a project.
        project_id = (await Project.create()).projectId
        # Add a collaborator.
        await ProjectCollaboration.create(
            project_id, COLLABORATOR_ID, True, True
        )
        # Test the invalid requests.
        await send_request_with_invalid_args(
            mcp, 'delete_project_collaborator', DeleteCollaboratorRequest,
            {
                'projectId': project_id,
                'collaboratorId': COLLABORATOR_ID
            },
            [
                # Try to delete a collaborator on a project that 
                # doesn't exist.
                {'projectId': -1},
                # Try to delete a collaborator on a project using an 
                # invalid user Id for the collaborator.
                {'collaboratorId': ' '}
            ]
        )
        # Remove the collaborators and delete the project to clean up.
        await ProjectCollaboration.delete(project_id, COLLABORATOR_ID)
        await Project.delete(project_id)
