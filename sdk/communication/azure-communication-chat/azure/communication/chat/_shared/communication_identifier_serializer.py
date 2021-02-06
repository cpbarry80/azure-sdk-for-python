# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from .models import (
    CommunicationIdentifierModel,
    CommunicationUserIdentifier,
    PhoneNumberIdentifier,
    MicrosoftTeamsUserIdentifier,
    UnknownIdentifier,
    CommunicationUserIdentifierModel,
    PhoneNumberIdentifierModel,
    MicrosoftTeamsUserIdentifierModel
)

class CommunicationUserIdentifierSerializer(object):

    @classmethod
    def serialize(cls, communicationIdentifier):
        """ Serialize the Communication identifier into CommunicationIdentifierModel

        :param identifier: Identifier object
        :type identifier: Union[CommunicationUserIdentifier,
           PhoneNumberIdentifier, MicrosoftTeamsUserIdentifier, UnknownIdentifier]
        :return: CommunicationIdentifierModel
        :rtype: ~azure.communication.chat.CommunicationIdentifierModel
        :raises Union[TypeError, ValueError]
        """
        if isinstance(communicationIdentifier, CommunicationUserIdentifier):
            return CommunicationIdentifierModel(
                communication_user=CommunicationUserIdentifierModel(id=communicationIdentifier.identifier)
            )
        if isinstance(communicationIdentifier, PhoneNumberIdentifier):
            return CommunicationIdentifierModel(
                raw_id=communicationIdentifier.raw_id,
                phone_number=PhoneNumberIdentifierModel(value=communicationIdentifier.phone_number)
            )
        if isinstance(communicationIdentifier, MicrosoftTeamsUserIdentifier):
            return CommunicationIdentifierModel(
                raw_id=communicationIdentifier.raw_id,
                microsoft_teams_user=MicrosoftTeamsUserIdentifierModel(user_id=communicationIdentifier.user_id,
                is_anonymous=communicationIdentifier.is_anonymous,
                cloud=communicationIdentifier.cloud)
            )

        if isinstance(communicationIdentifier, UnknownIdentifier):
            return CommunicationIdentifierModel(
                raw_id=communicationIdentifier.identifier
            )

        raise TypeError("Unsupported identifier type " + communicationIdentifier.__class__.__name__)

    @classmethod
    def deserialize(cls, identifierModel):
        """
        Deserialize the CommunicationIdentifierModel into Communication Identifier

        :param identifierModel: CommunicationIdentifierModel
        :type identifierModel: CommunicationIdentifierModel
        :return: Union[CommunicationUserIdentifier, CommunicationPhoneNumberIdentifier]
        :rtype: Union[CommunicationUserIdentifier, CommunicationPhoneNumberIdentifier]
        :rasies: ValueError
        """

        raw_id = identifierModel.raw_id
        if not raw_id:
            raise ValueError("Identifier must have a valid id")

        if identifierModel.communication_user is not None:
            return CommunicationUserIdentifier(raw_id)
        if identifierModel.phone_number is not None:
            if not identifierModel.phone_number:
                raise ValueError("PhoneNumberIdentifier must have a valid attribute - phone_number")
            return PhoneNumberIdentifier(identifierModel.phone_number.value, raw_id=raw_id)
        if identifierModel.microsoft_teams_user is not None:
            if identifierModel.microsoft_teams_user.is_anonymous not in [True, False]:
                raise ValueError("MicrosoftTeamsUser must have a valid attribute - is_anonymous")
            if not identifierModel.microsoft_teams_user.user_id:
                raise ValueError("MicrosoftTeamsUser must have a valid attribute - microsoft_teams_user_id")
            if not identifierModel.microsoft_teams_user.cloud:
                raise ValueError("MicrosoftTeamsUser must have a valid attribute - communication_cloud_environment")
            return MicrosoftTeamsUserIdentifier(
                raw_id=raw_id,
                user_id=identifierModel.microsoft_teams_user.user_id,
                is_anonymous=identifierModel.microsoft_teams_user.is_anonymous,
                cloud=identifierModel.microsoft_teams_user.cloud
            )

        return UnknownIdentifier(raw_id)
