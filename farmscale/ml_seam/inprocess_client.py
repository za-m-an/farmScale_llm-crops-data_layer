"""In-process MLClient stub for direct integration with the Layer 3 `ml` package."""

from __future__ import annotations

from typing import Any


class InProcessMLClient:
    """
    Stub client that imports `ml.*` lazily.
    This is the ONLY file in FarmScale allowed to import `ml.*`.
    """

    def _load_ml_module(self) -> Any:
        try:
            # TODO(integration): replace with the actual Layer 3 entrypoint module, e.g.:
            # import ml.service as ml_service
            import ml  # type: ignore[import-not-found]

            return ml
        except ImportError as exc:
            raise RuntimeError(
                "In-process ML package 'ml' is not installed or not on PYTHONPATH. "
                "Use ML_MODE=mock or ML_MODE=http, or integrate the Layer 3 'ml' package "
                "in ml_seam/inprocess_client.py."
            ) from exc

    def rank(self, request: dict[str, Any]) -> dict[str, Any]:
        ml_mod = self._load_ml_module()
        # TODO(integration): call the real Layer 3 ranking function, e.g.:
        # return ml_mod.rank_rotations(
        #     district=request["district"],
        #     upazila=request["upazila"],
        #     latitude=request["latitude"],
        #     longitude=request["longitude"],
        #     goal=request["goal"],
        #     season=request.get("season", "annual"),
        #     language=request.get("language", "en"),
        #     top_k=request.get("top_k", 3),
        #     candidate_crops=request.get("candidate_crops"),
        # )
        if hasattr(ml_mod, "rank"):
            return ml_mod.rank(request)
        raise RuntimeError("Loaded 'ml' package does not expose rank(request). Update TODO(integration) in ml_seam/inprocess_client.py.")

    def health(self) -> dict[str, Any]:
        try:
            self._load_ml_module()
            return {"status": "ok", "mode": "inprocess"}
        except RuntimeError as exc:
            return {"status": "unavailable", "mode": "inprocess", "error": str(exc)}
