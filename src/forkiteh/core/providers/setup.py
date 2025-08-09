from dishka import make_async_container

from forkiteh.core.providers.infrastructure_provider import InfrastructureProvider
from forkiteh.core.providers.repositories_provider import RepositoriesProvider
from forkiteh.core.providers.services_provider import ServicesProvider
from forkiteh.core.providers.use_cases_provider import UseCasesProvider

app_container = make_async_container(
    InfrastructureProvider(),
    RepositoriesProvider(),
    ServicesProvider(),
    UseCasesProvider(),
)
