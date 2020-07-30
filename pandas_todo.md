# Pandas Related Issues

## Bug in merge

Repro: 

1. Attempt to turn the code of `GraphTraversal.out()` into `GraphTraversal.in_()`:
```python
    def in_(self):
        """
        :returns: A GraphTraversal that adds the destination of any edges into
        the current traversal's last element.
        """
        if self._path_col_types[-1] != "v":
            raise ValueError(
                "Can only call out() when the last element in the path is a "
                "vertex. Last element type is {}".format(
                    self._path_col_types[-1]))

        # Column of path is a list of vertices. Join with edges table.
        p = self.paths
        new_paths = (
            p
            .merge(self.edges, left_on=p.columns[-1], right_on="to")
            .drop("to",
                  axis="columns")  # merge keeps both sides of equijoin
            .rename(columns={
                "from": len(p.columns)}))  # "from" field ==> Last element
        new_path_col_types = self._path_col_types + ["v"]
        return GraphTraversal(self.vertices, self.edges, new_paths,
                              new_path_col_types, self._aliases)
```
2. Attempt to call the `in_()` method:
```python
import pandas_text.gremlin.convert
g = pandas_text.gremlin.convert.token_features_to_traversal(token_features)
g.V().in_().toList()
```
You will get a strange error message about inputs to assign not being strings.
