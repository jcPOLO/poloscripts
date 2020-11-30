from typing import Any, Dict, Optional, List
from nornir.core.filter import F


class FilterInventory:

    def __init__(
            self,
            host: Optional[Host] = None,
            filter_parameters: Optional[Dict[str, Any]] = None,
            ** kwargs: Any,

    ) -> None:
        filter_parameters = filter_parameters or {}
        self.filter_parameters = filter_parameters

    def show_filtering_options(self, fields: Dict[str]):
        birds = nr.filter(F(groups__contains="bird"))
        print(birds.inventory.hosts.keys())
        pass

    def filter_by(self, fields: List[str], text: str):
        pass
