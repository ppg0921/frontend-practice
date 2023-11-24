import { ApolloClient, InMemoryCache, HttpLink, split } from "@apollo/client";
import { getMainDefinition } from "@apollo/client/utilities";
import { createClient } from "graphql-ws";
import { GraphQLWsLink } from "@apollo/client/link/subscriptions";
import { COLOR_MUTATION_SUB, Color } from "../graphql";

const HOST = "http://localhost:4000";

const wsLink = new GraphQLWsLink(
  createClient({
    url: `${HOST}/graphql`.replace("http", "ws"),
  })
);
// the url of graphql itself
const httpLink = new HttpLink({
  uri: `${HOST}/graphql`,
});

// know whether the url belongs to socket or http
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  wsLink,
  httpLink,
)

const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache({
    // operations when the values in cache are modified or when the values are read(not covered in the code)
    typePolicies: {
      Query: {
        fields: {
          colors: {
            merge(existing, incoming) {
              return incoming;
              // choose to store the new data after new cache value is formed
              // if return [], the cache will be cleared
              // this function is used when we have some fat data, and the copy of such fat data should be avoided
            },
          },
        },
      },
    },
  }),
  connectToDevTools: process.env.NODE_ENV !== "production",
});

enum ColorMutationType {
  CREATED = "CREATED",
  UPDATED = "UPDATED",
  DELETED = "DELETED",
}

client.subscribe({
  query: COLOR_MUTATION_SUB,
})
  .subscribe({
    next: ({ data }) => {
      const { color, colorCode, mutation } = data.colorMutated;
      const newColor: Color = { color, colorCode };
      console.log(`Color ${color} ${mutation}: ${colorCode}`);
      client.cache.modify({
        fields: {
          // existingColors: original query result stored in cache
          // return new query result so that we can get the correct value the next time we want to query
          colors: (existingColors) => {
            switch (mutation) {
              case ColorMutationType.CREATED:
                return [...existingColors, data.colorMutated];
              case ColorMutationType.UPDATED:
                return existingColors.map((color: Color) => {
                  if (color.color === data.colorMutated.color) {
                    return data.colorMutated;
                  }
                  return color;
                });
              case ColorMutationType.DELETED:
                return existingColors.filter(
                  (color: Color) => color.color !== data.colorMutated.color
                );
              default:
                return existingColors;
            }
          },
        },
      });
    },
    error: (err) => console.error(err),
  });

export default client;