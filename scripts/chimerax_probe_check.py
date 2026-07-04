from chimerax.core.commands import run

session = session  # noqa: F821

run(session, "open data/raw/1SEZ.pdb")
run(session, "measure sasa")  # default probe radius
run(session, "measure sasa probeRadius 1.4")  # explicit standard water radius
run(session, "measure sasa probeRadius 1.4 sum /A:98")  # R98 specifically, summed
run(session, "exit")
