function getPageNameFromPath() {
    const currentPath = window.location.pathname;
    const trimmedPath = currentPath.startsWith('/') ? currentPath.substring(1) : currentPath;
    const trimmedEndPath = trimmedPath.endsWith('/') ? trimmedPath.slice(0, -1) : trimmedPath;
    const pathSegments = trimmedEndPath.split('/');
    const pageName = pathSegments.length > 0 ? pathSegments[pathSegments.length - 1] : '';
    return pageName;
}

export { getPageNameFromPath }
      