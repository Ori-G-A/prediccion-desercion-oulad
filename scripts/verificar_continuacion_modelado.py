"""Comprueba que un fallo de selección impide congelar o abrir prueba."""
import tempfile
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import continuar_protocolo_modelado as flow


class ContinuationTests(unittest.TestCase):
    def test_progress_timeout_does_not_stop_supervision(self):
        with patch.object(flow.subprocess, 'run', side_effect=subprocess.TimeoutExpired('contador', 30)), \
                patch.object(flow, 'record') as record:
            flow.progress()
            self.assertEqual(record.call_args.args[:2], (1, 'incidencia_registro_progreso'))

    def setUp(self):
        folder = flow.ROOT/'tmp/pruebas_continuacion'
        folder.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=folder)
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def test_failure_stops_before_freeze_and_test(self):
        calls = []
        def fail_selection(stage, script, *args):
            calls.append(stage)
            if stage == 2:
                raise ValueError('Pliegue incompleto simulado')
        with patch.object(flow, 'ROOT', self.root), patch.object(flow, 'REPORT', self.root), \
                patch.object(flow, 'run', side_effect=fail_selection), patch.object(flow, 'record'), \
                patch.object(flow, 'checkpoint') as checkpoint:
            with self.assertRaisesRegex(ValueError, 'incompleto'):
                flow.main(None)
            self.assertEqual(calls, [1, 2])
            checkpoint.assert_not_called()
        self.assertFalse((self.root/'continuacion.lock').exists())

    def test_opened_test_prevents_new_training(self):
        marker = self.root/'reportes/continuacion_modelado_2026_10_19/primera_apertura_prueba.json'
        marker.parent.mkdir(parents=True)
        marker.write_text('{}', encoding='utf-8')
        with patch.object(flow, 'ROOT', self.root), patch.object(flow, 'REPORT', self.root), \
                patch.object(flow, 'run') as run, patch.object(flow, 'record'):
            with self.assertRaisesRegex(RuntimeError, 'ya fue abierta'):
                flow.main(None)
            run.assert_not_called()

    def test_exclusive_supervisor(self):
        (self.root/'continuacion.lock').write_text('existing', encoding='utf-8')
        with patch.object(flow, 'REPORT', self.root), patch.object(flow, 'run') as run:
            with self.assertRaises(FileExistsError):
                flow.main(None)
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
