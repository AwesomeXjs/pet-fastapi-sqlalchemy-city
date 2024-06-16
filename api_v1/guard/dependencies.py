from fastapi import HTTPException, Request, status


class ApiGuard:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, request: Request):
        if "admin" not in request.cookies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"У вас недостаточно прав"
            )
        # логика для валидации куки и отдача нужной информации
        return True


api_guard = ApiGuard("payments")
