from domain import TonalSystem, Scale, TonalSystemElement

z12 = TonalSystem(12)

z12.set_generator(7)
diatonic = z12.diatonic_scale()
print(diatonic.interval_struct)
print(diatonic.interval_vector)
print([e.value for e in diatonic.elements])

diatonic.set_tonic(5)
print([e.value for e in diatonic.elements])

diatonic.export_scala_files("fa_scale.scl")

octa = z12.scale([0, 2, 3, 5, 6, 8, 9, 11])
print(octa.interval_struct)
print(octa.interval_vector)
print([e.value for e in octa.elements])