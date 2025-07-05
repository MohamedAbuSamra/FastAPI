from .auth import router as auth_router
from .products import router as products_router
from .orders import router as orders_router
from .countries import router as countries_router
from .users import router as users_router

all_routers = [
    auth_router,
    products_router,
    orders_router,
    countries_router,
    users_router,
] 