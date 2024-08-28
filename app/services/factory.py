from app.services.start import Start

class ServiceFactory:

    async def create_start(self) -> Start:
        return Start('start service')

