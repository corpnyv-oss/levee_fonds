import logging
from typing import Dict, Any, BinaryIO

try:
    import pyclamd
except Exception:
    pyclamd = None

LOGGER = logging.getLogger(__name__)


def scan_file(file: BinaryIO) -> Dict[str, Any]:
    """Scan the uploaded file with ClamAV and return a result dict.

    Returns:
        {'infected': bool, 'reason': str|None}
    """
    if pyclamd is None:
        LOGGER.debug("pyclamd not installed; skipping ClamAV scan")
        return {'infected': False, 'reason': 'pyclamd_not_installed'}

    cd = None
    # try network socket then unix socket
    try:
        try:
            cd = pyclamd.ClamdNetworkSocket()
            cd.ping()
        except Exception:
            cd = pyclamd.ClamdUnixSocket()
            cd.ping()
    except Exception:
        LOGGER.warning("ClamAV daemon not reachable; skipping scan")
        return {'infected': False, 'reason': 'scanner_unavailable'}

    # Safely read file content and restore pointer
    try:
        try:
            file.seek(0)
        except Exception:
            pass
        content = file.read()
    except Exception as e:
        LOGGER.exception("Failed to read uploaded file for ClamAV scan: %s", e)
        return {'infected': False, 'reason': 'read_error'}
    finally:
        try:
            file.seek(0)
        except Exception:
            pass

    # Determine scan function available on pyclamd object
    scan_fn = getattr(cd, 'scan_buffer', None) or getattr(cd, 'scan_stream', None) or getattr(cd, 'scan_file', None)
    if not callable(scan_fn):
        LOGGER.warning("No compatible scan function found on ClamAV client")
        return {'infected': False, 'reason': 'no_scan_function'}

    try:
        # Some implementations expect bytes, others a stream; pass bytes for buffer/stream scans
        result = scan_fn(content)
    except Exception as e:
        LOGGER.exception("ClamAV scan error: %s", e)
        return {'infected': False, 'reason': 'scan_error'}

    if result:
        return {'infected': True, 'reason': str(result)}

    return {'infected': False, 'reason': None}
