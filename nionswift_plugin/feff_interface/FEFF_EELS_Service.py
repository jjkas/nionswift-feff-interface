import typing
import importlib
import numpy
from nion.eels_analysis import EELS_CrossSections
from nion.utils import Registry


class EELSAnalysisService:
    def energy_diff_cross_section_nm2_per_eV(self, atomic_number: int, shell_number: int, subshell_index: int,
                                             edge_onset_eV: float, edge_delta_eV: float, beam_energy_eV: float,
                                             convergence_angle_rad: float, collection_angle_rad: float) -> numpy.ndarray:
        
        from nion.eels_analysis.PeriodicTable import ElectronShell, PeriodicTable
        atomic_eels_loader = importlib.util.find_spec('atomic_eels')
        if atomic_eels_loader is not None:
            import atomic_eels
            #from atomic_eels import atomic_diff_cross_section
        else:
            return None

        #shell_init = ElectronShell(atomic_number,shell_number,subshell_index)
        ptable = PeriodicTable()

        # J. Kas
        # Now get a list of shells for this atomic species for which the edge
        # energy is within the energy range specified by edge_onset_eV to
        # edge_onset + edge_delta_eV
        energy_margin = 10.0 # Chemical shifts can make theoretical edge +/- 10eV of experimental.
        energy_interval_eV = (edge_onset_eV-energy_margin, edge_onset_eV + edge_delta_eV)
        shells = ptable.find_edges_in_energy_interval(energy_interval_eV)
        assert len(shells) > 0, "No edges for this atom in energy range specified. Atomic #: "  + str(atomic_number)

        energy_step = 0.1  # Set small energy step for now. Adjust later depending on core-hole broadening.
        egrid_eV = numpy.arange(edge_onset_eV, edge_onset_eV + edge_delta_eV, 0.1) # Define energy grid
        energyDiffSigma_total = numpy.zeros_like(egrid_eV) # Initialize total cross section.
        
        # Loop over shells in energy range and get total cross section.
        for shell in shells:
            if shell.atomic_number == atomic_number:
                edge_label = shell.get_shell_str_in_eels_notation(include_subshell=True)
                beam_energy_keV = beam_energy_eV/1000.0
                convergence_angle_mrad = convergence_angle_rad*1000.0
                collection_angle_mrad = collection_angle_rad*1000.0
                energyDiffSigma,edge_energy = atomic_eels.atomic_diff_cross_section(atomic_number, edge_label, beam_energy_keV,
                                                                                    convergence_angle_mrad, collection_angle_mrad, egrid_eV)
                energyDiffSigma_total = numpy.add(energyDiffSigma_total,energyDiffSigma)

        return energyDiffSigma_total

        
Registry.register_component(EELSAnalysisService(), {"eels_analysis_service"})
