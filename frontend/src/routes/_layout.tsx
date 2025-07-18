import { Flex } from "@chakra-ui/react"
import { Outlet, createFileRoute, redirect } from "@tanstack/react-router"

import Navbar from "@/components/Common/Navbar"
import Sidebar from "@/components/Common/Sidebar"
import { isLoggedIn } from "@/hooks/useAuth"
import { Nav } from "@/components/Common/NewNav"

export const Route = createFileRoute("/_layout")({
  component: Layout,
  beforeLoad: async () => {
    if (!isLoggedIn()) {
      throw redirect({
        to: "/login",
      })
    }
  },
})

function Layout() {
  return (
    <>
      <Nav />
      <div className="container mx-auto px-4 pt-14 text-sm">
        <div className="bg-background">
          <Flex direction="column" h="100vh">
            <Flex flex="1" overflow="hidden">
              <Sidebar />
              <Flex flex="1" direction="column" p={4} overflowY="auto">
                <Outlet />
              </Flex>
            </Flex>
          </Flex>
        </div>
      </div>
    </>
  )
}

export default Layout
