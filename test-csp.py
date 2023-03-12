from backup import GraphColoringCSP

import unittest


class GraphColoringCSPTestCase(unittest.TestCase):

    def test_graph_validity(self):
        # Test that the constructor raises an error if the graph is invalid
        graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: {5}, 5: {4}}
        num_colors = 3
        with self.assertRaises(ValueError):
            GraphColoringCSP(graph, num_colors)

    def test_MRVgetUnassignedArea(self):
        # Test the MRVgetUnassignedArea method
        graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: {5}, 5: {4}}
        num_colors = 3
        csp = GraphColoringCSP(graph, num_colors)
        color_map = {1: 0, 2: 1}
        unassigned = csp.MRVgetUnassignedArea(color_map)
        self.assertEqual(unassigned, 3)

    def test_LCVgetOrderedDomainValues(self):
        # Test the LCVgetOrderedDomainValues method
        graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: {5}, 5: {4}}
        num_colors = 3
        csp = GraphColoringCSP(graph, num_colors)
        color_map = {1: 0, 2: 1}
        ordered_values = csp.LCVgetOrderedDomainValues(3, color_map)
        self.assertEqual(ordered_values, [2, 0, 1])

    def test_countConflicts(self):
        # Test the countConflicts method
        graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: {5}, 5: {4}}
        num_colors = 3
        csp = GraphColoringCSP(graph, num_colors)
        color_map = {1: 0, 2: 1}
        conflicts = csp.countConflicts(3, 0, color_map)
        self.assertEqual(conflicts, 1)
      
    def test_isValidColor(self):
        # Test the isValidColor method
        graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: {5}, 5: {4}}
        num_colors = 3
        csp = GraphColoringCSP(graph, num_colors)
        color_map = {1: 0, 2: 1}
        
        # Test a valid color assignment
        result = csp.isValidColor(4, 0, color_map)
        self.assertTrue(result)

    def test_AC3(self):
        # Test the AC3 method
        graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: {5}, 5: {4}}
        num_colors = 3
        csp = GraphColoringCSP(graph, num_colors)
        csp.domain = {1: {0, 1, 2}, 2: {0, 1, 2}, 3: {0, 1}, 4: {0, 1, 2}, 5: {0, 1, 2}}
        csp.AC3()
        self.assertEqual(csp.domain[1], {2})
        self.assertEqual(csp.domain[2], {2})
        self.assertEqual(csp.domain[3], {1})
        self.assertEqual(csp.domain[4], {2})
        self.assertEqual(csp.domain[5], {0, 1, 2})

    def test_removeInconsistentValues(self):
        # Test the removeInconsistentValues method
        graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: {5}, 5: {4}}
        num_colors = 3
        csp = GraphColoringCSP(graph, num_colors)
        csp.domain = {1: {0, 1, 2}, 2: {0, 1, 2}, 3: {0, 1}, 4: {0, 1, 2}, 5: {0, 1, 2}}
        removed = csp.revise(1, 2)
        self.assertTrue(removed)
        self.assertEqual(csp.domain[1], {1, 2})
       
class TestBackTrackAlgorithm(unittest.TestCase):
    def setUp(self):
        # Create a graph for testing
        self.graph = {
            1: {2, 3},
            2: {1, 3},
            3: {1, 2},
            4: {5},
            5: {4}
        }
        self.num_colors = 3
    
    def test_backtrack(self):
        # Test the backtrack function
        csp = GraphColoringCSP(self.graph, self.num_colors)
        solution = csp.backtrack({})
        # Check that all vertices are colored
        self.assertEqual(len(solution), len(self.graph))
        # Check that adjacent vertices have different colors
        for vertex in self.graph:
            for neighbor in self.graph[vertex]:
                self.assertNotEqual(solution[vertex], solution[neighbor])
    
    def test_backtrack_with_initial_assignment(self):
        # Test the backtrack function with an initial assignment
        initial_assignment = {1: 0, 2: 1, 3: 2}
        csp = GraphColoringCSP(self.graph, self.num_colors)
        solution = csp.backtrack(initial_assignment)
        # Check that all vertices are colored
        self.assertEqual(len(solution), len(self.graph))
        # Check that the initial assignment is respected
        for vertex, color in initial_assignment.items():
            self.assertEqual(solution[vertex], color)
        # Check that adjacent vertices have different colors
        for vertex in self.graph:
            for neighbor in self.graph[vertex]:
                self.assertNotEqual(solution[vertex], solution[neighbor])
    
    def test_backtrack_no_solution(self):
        # Test that the backtrack function correctly returns None when there is no solution
        graph = {1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4}, 4: {2, 3}}
        num_colors = 2
        csp = GraphColoringCSP(graph, num_colors)
        solution = csp.backtrack({})
        self.assertIsNone(solution)

    def test_forwardChecking(self):
        # Test the forwardChecking method
        graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: {5}, 5: {4}}
        num_colors = 3
        csp = GraphColoringCSP(graph, num_colors)
        color_map = {1: 0, 2: 1}
        inferences = csp.forwardChecking(1, 0, color_map)
        self.assertEqual(len(inferences), 1)
        self.assertEqual(inferences[0], (3, 0))

    def test_undoForwardChecking(self):
        # Test the undoForwardChecking method
        graph = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: {5}, 5: {4}}
        num_colors = 3
        csp = GraphColoringCSP(graph, num_colors)
        csp.domain = {1: {0, 1, 2}, 2: {0, 1, 2}, 3: {0, 1}, 4: {0, 1}, 5: {0, 1, 2}}
        inferences = [(2, 0), (3, 2)]
        csp.undoForwardChecking(inferences)
        self.assertEqual(csp.domain[1], {0, 1, 2})
        self.assertEqual(csp.domain[2], {0, 1, 2})
        self.assertEqual(csp.domain[3], {0, 1, 2})
       
if __name__ == '__main__':
    unittest.main()