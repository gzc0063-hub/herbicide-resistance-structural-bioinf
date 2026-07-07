// Mirrors scripts/build_review_driven_outputs.py's COLORS dict exactly, so the
// site's charts use the same palette as the manuscript's SVG figures.
export const COLORS = {
  ACCase: '#3f6fb5',
  ALS: '#44935f',
  EPSPS: '#c28b2c',
  PPO: '#9b4d8b',
  direct_core: '#2f6fbb',
  adjacent: '#46945f',
  second_shell_channel: '#2f9fa8',
  allosteric_hinge: '#c77f2f',
  interface_induced_fit: '#7b5bc6',
  unresolved_static_candidate: '#777777',
  random: '#c8c8c8',
}

export const MECHANISM_LABELS = {
  direct_core: 'Direct core',
  adjacent: 'Adjacent',
  second_shell_channel: 'Second-shell / channel',
  allosteric_hinge: 'Allosteric hinge',
  interface_induced_fit: 'Interface induced-fit',
  unresolved_static_candidate: 'Unresolved',
}

export const REPO_URL = 'https://github.com/gzc0063-hub/herbicide-resistance-structural-bioinf'
