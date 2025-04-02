import logging
import random
from uuid import UUID
import json

from faker import Faker
from pathlib import Path
from app.core.user.models import User
from app.core.user.repository import UserRepository
from app.core.user.schemas import UserIn
from app.database.dependencies import get_db_session
from app.database.exceptions import DuplicateEntryError

logger = logging.getLogger("Test Users")

# Inicializa o Faker para gerar dados fictícios
fake = Faker()

# Lista para armazenar os IDs dos usuários de teste criados
USER_IDS_FILE = Path("app/tests/test_users.json")

async def generate_fake_users(num_users: int = 10) -> None:
    """
    :param num_users: Número de usuários a serem gerados.
    """
    for _ in range(num_users):
        # Gera os dados fictícios para o usuário
        user_in = UserIn(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(length=10),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        # Cria o usuário usando a função existente
        user = await create_user(user_in)
        test_user_ids = []
        test_user_ids.append(user.id)
        # Registra o ID do usuário criado
        save_test_user_ids(test_user_ids)

    print(f"{num_users} usuários fictícios criados via create_user!")


async def create_user(user_in: UserIn):
    try:
        async for session in get_db_session():
            user_repository = UserRepository(session, User)
            user = await user_repository.create(user_in)

            if random.choice([True, False]):
                async for session in get_db_session():
                    user.soft_delete()
            
            await user_repository.save(obj=user)
    except DuplicateEntryError as e:
        logger.debug(e)
    except Exception as e:
        logger.error(f"Error on user creation \n userIn: {user_in}\n{e}")
        raise e
    return user


def save_test_user_ids(user_ids: list[UUID]) -> None:
    """
    Salva os IDs dos usuários de teste em um arquivo JSON.
    """
    with open(USER_IDS_FILE, "w") as f:
        json.dump([str(uid) for uid in user_ids], f)

