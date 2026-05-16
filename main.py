from python_topology import Graph, Thickening, SphereWithHandles, Hieroglyph


def example_1_graphs_and_genus():
    print("=== Пример 1: Графы и их минимальный род ===")

    k4 = Graph(4, [[] for _ in range(4)])
    for i in range(4):
        for j in range(i + 1, 4):
            k4.add_edge(i, j)

    print(f"Минимальный род графа K4: {k4.handles()} (Ожидается 0 - Сфера)")

    k5 = Graph(5, [[] for _ in range(5)])
    for i in range(5):
        for j in range(i + 1, 5):
            k5.add_edge(i, j)

    print(f"Минимальный род графа K5: {k5.handles()} (Ожидается 1 - Тор)\n")


def example_2_manifolds_and_homeomorphisms():
    print("=== Пример 2: Многообразия и Гомеоморфизмы ===")

    torus_explicit = SphereWithHandles(1, 0)
    torus_word = Hieroglyph("abAB")

    print(f"{torus_explicit} гомеоморфен {torus_word} ? -> {torus_explicit.is_homeomorphic_to(torus_word)}")

    klein_explicit = SphereWithHandles(0, 0, 2)
    klein_word = Hieroglyph("aabb")

    print(f"Бутылка Клейна гомеоморфна иероглифу 'aabb' ? -> {klein_explicit.is_homeomorphic_to(klein_word)}\n")


def example_3_connected_sums():
    print("=== Пример 3: Связная сумма (Сложение поверхностей) ===")

    torus1 = SphereWithHandles(1, 0)
    torus2 = SphereWithHandles(1, 0)

    double_torus = torus1 + torus2
    print(f"Тор + Тор = {double_torus}")

    projective_plane = SphereWithHandles(0, 0, 1)
    dick_surface = torus1 + projective_plane
    print(f"Тор + Проективная плоскость = {dick_surface} (Ожидается 0 ручек, 3 пленки Мёбиуса)\n")


def example_4_realizability():
    print("=== Пример 4: Реализуемость (Вложение графа в поверхность) ===")

    k5 = Graph(5, [[] for _ in range(5)])
    for i in range(5):
        for j in range(i + 1, 5):
            k5.add_edge(i, j)

    sphere = SphereWithHandles(0, 0)
    torus = SphereWithHandles(1, 0)

    print(f"Можно ли нарисовать K5 на Сфере без пересечений? -> {sphere.is_realizable(k5)}")
    print(f"Можно ли нарисовать K5 на Торе без пересечений? -> {torus.is_realizable(k5)}\n")


def example_5_thickenings_and_euler():
    print("=== Пример 5: Утолщения (Ленточные графы) и Формула Эйлера ===")

    k4 = Graph(4, [[] for _ in range(4)])
    for i in range(4):
        for j in range(i + 1, 4):
            k4.add_edge(i, j)

    t = Thickening(k4, 0)

    print(f"Выбрано утолщение графа: {t}")
    print(f"Количество дырок (граничных циклов): {t.holes()}")
    print(f"Род данного утолщения: {t.handles()}")

    try:
        t.validate_euler_formula()
        print("Формула Эйлера V - E + F = 2 - 2g успешно выполнена!")
    except Exception as e:
        print(f"Ошибка Эйлера: {e}")

example_1_graphs_and_genus()
example_2_manifolds_and_homeomorphisms()
example_3_connected_sums()
example_4_realizability()
example_5_thickenings_and_euler()