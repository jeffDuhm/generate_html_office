from docx import Document
from fastapi import UploadFile
from sqlalchemy.orm import Session

from converter import WordToHtmlConverter
from corepy.shared.logging.logging import Logger
from corepy.shared.schemas.response_schemas import ResponseSuccessSchema
from corepy.site.site_queries import SiteQueries
from corepy.site.site_exceptions import SiteNotFoundError
from corepy.site_config.site_config_usecases import SiteConfigUsecases
from corepy.conversion_log.conversion_log_queries import ConversionLogQueries
from corepy.conversion.conversion_schemas import ConversionResultSchema
from corepy.conversion.conversion_exceptions import NoFilesError, InvalidFileTypeError
from corepy.conversion.conversion_messages import SuccessConversionMessages


class ConversionUsecases:

    def __init__(self, db: Session):
        self.db = db
        self.logger = Logger(__name__)

    def convert(
        self,
        user_id: int,
        site_id: int,
        files: list[UploadFile],
        use_sections: bool = True,
    ) -> ResponseSuccessSchema:

        site = SiteQueries(self.db).get_by_id(site_id)
        if not site or not site.is_active:
            raise SiteNotFoundError()

        if not files:
            raise NoFilesError()

        for upload_file in files:
            filename = upload_file.filename or ""
            if not filename.lower().endswith(".docx"):
                raise InvalidFileTypeError()

        rules = SiteConfigUsecases(self.db).get_rules(
            user_id=user_id,
            site_id=site_id,
            use_sections=use_sections,
        )
        log_queries = ConversionLogQueries(self.db)

        results = []
        for upload_file in files:
            filename = upload_file.filename
            try:
                document = Document(upload_file.file)
                converter = WordToHtmlConverter(document, rules)
                html = converter.convert()

                result = ConversionResultSchema(
                    filename=filename,
                    status="success",
                    html=html,
                    error=None
                )
                log_queries.create(
                    user_id=user_id,
                    site_id=site_id,
                    filename=filename[:255],
                    status="success",
                    error_message=None
                )
            except Exception as e:
                self.logger.error(f"Error converting {filename}: {e}")
                error_message = "The file could not be converted"

                result = ConversionResultSchema(
                    filename=filename,
                    status="error",
                    html=None,
                    error=error_message
                )
                log_queries.create(
                    user_id=user_id,
                    site_id=site_id,
                    filename=filename[:255],
                    status="error",
                    error_message=error_message
                )

            results.append(result.model_dump())

        return ResponseSuccessSchema(
            message=SuccessConversionMessages.CONVERSION_COMPLETED,
            data=results
        )