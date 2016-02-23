import logging

from lcmap.client.api import base, routes


log = logging.getLogger(__name__)

#context = routes.models_context + "/ccdc"
context = routes.models_context + "/ccdc/piped-processes"

class CCDCPipedProcesses(base.APIComponent):

    def run(self, spectra="", x_val="", y_val="", start_time="", end_time="",
            row="", col="", in_dir="", out_dir="", scene_list="", verbose=""):
        return self.http.post(context, data={
            "spectra": spectra,
            "x-val": x_val,
            "y-val": y_val,
            "start-time": start_time,
            "end-time": end_time,
            "row": row,
            "col": col,
            "in-dir": in_dir,
            "out-dir": out_dir,
            "scene-list": scene_list,
            "verbose": verbose})

